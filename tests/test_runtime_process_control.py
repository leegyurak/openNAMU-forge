from opennamu_forge.presentation.runtime import process_control


class FakeThread:
    def __init__(self, target, daemon):
        self.target = target
        self.daemon = daemon
        self.started = False

    def start(self):
        self.started = True


def test_build_python_restart_candidates는_현재_python_후보를_반환한다():
    candidates = process_control.build_python_restart_candidates(
        executable="/venv/bin/python",
        major=3,
        minor=10,
    )

    assert candidates == (
        "/venv/bin/python",
        "python3.10",
        "python3",
        "python",
        "py -3.10",
    )


def test_restart_current_process는_argv를_전달하고_종료한다():
    calls = []
    exits = []

    def fake_popen(cmd):
        calls.append(cmd)
        return object()

    def fake_exit(code):
        exits.append(code)

    process_control.restart_current_process(
        ("app.py", "--dev"),
        exit_process=fake_exit,
        popen=fake_popen,
        sleep=lambda seconds: calls.append(["sleep", str(seconds)]),
    )

    assert calls == [["sleep", "3"], [process_control.sys.executable, "app.py", "--dev"]]
    assert exits == [0]


def test_restart_current_process는_실패한_python_후보를_건너뛴다(monkeypatch):
    calls = []
    monkeypatch.setattr(process_control, "build_python_restart_candidates", lambda: ("bad-python", "good-python"))

    def fake_popen(cmd):
        calls.append(cmd)
        if cmd[0] == "bad-python":
            raise OSError
        return object()

    process_control.restart_current_process(
        ("app.py",),
        exit_process=lambda code: calls.append(["exit", str(code)]),
        popen=fake_popen,
        sleep=lambda seconds: None,
    )

    assert calls == [["bad-python", "app.py"], ["good-python", "app.py"], ["exit", "0"]]


def test_schedule_restart는_daemon_thread를_시작한다(monkeypatch):
    calls = []

    def fake_thread(target, daemon):
        thread = FakeThread(target, daemon)
        calls.append(thread)
        return thread

    monkeypatch.setattr(process_control.threading, "Thread", fake_thread)

    thread = process_control.schedule_restart()

    assert thread is calls[0]
    assert thread.target is process_control.restart_current_process
    assert thread.daemon is True
    assert thread.started is True


def test_shutdown_current_process는_exit_process를_호출한다():
    calls = []

    process_control.shutdown_current_process(exit_process=lambda: calls.append("exit"))

    assert calls == ["exit"]


def test_register_termination_handlers는_signal과_atexit을_등록한다():
    signal_calls = []
    atexit_calls = []
    runtime_calls = []
    process = object()

    def fake_signal(signal_number, handler):
        signal_calls.append((signal_number, handler))

    def fake_atexit_register(func, registered_process):
        atexit_calls.append((func, registered_process))

    def fake_terminate(registered_process):
        runtime_calls.append(("terminate", registered_process))

    def fake_exit(code):
        runtime_calls.append(("exit", code))

    process_control.register_termination_handlers(
        process,
        fake_terminate,
        signal_func=fake_signal,
        atexit_register=fake_atexit_register,
        exit_process=fake_exit,
    )
    signal_calls[0][1](process_control.signal.SIGTERM, None)

    assert signal_calls[0][0] == process_control.signal.SIGTERM
    assert signal_calls[1][0] == process_control.signal.SIGINT
    assert atexit_calls == [(fake_terminate, process)]
    assert runtime_calls == [("terminate", process), ("exit", 0)]
