import subprocess
from types import SimpleNamespace

from opennamu_forge.presentation.runtime import gopennamu_process


class FakeProcess:
    def __init__(self):
        self.terminated = False
        self.killed = False
        self.wait_calls = 0

    def terminate(self):
        self.terminated = True

    def kill(self):
        self.killed = True

    def poll(self):
        return None

    def wait(self, timeout=None):
        self.wait_calls += 1
        if self.wait_calls == 1:
            raise subprocess.TimeoutExpired("main.bin", float(timeout or 0))
        return 0


def test_kill_port는_listen_pid를_종료하고_정렬해_반환한다(monkeypatch):
    process = FakeProcess()
    connection = SimpleNamespace(pid=20, laddr=SimpleNamespace(port=3001), status="LISTEN")
    monkeypatch.setattr(gopennamu_process.psutil, "CONN_LISTEN", "LISTEN")
    monkeypatch.setattr(gopennamu_process.psutil, "net_connections", lambda kind: (connection,))
    monkeypatch.setattr(gopennamu_process.psutil, "Process", lambda pid: process)
    monkeypatch.setattr(gopennamu_process.psutil, "wait_procs", lambda procs, timeout: ((), (process,)))

    killed = gopennamu_process.kill_port("3001")

    assert killed == [20]
    assert process.terminated is True
    assert process.killed is True


def test_start_gopennamu_process는_기존_인자를_그대로_전달한다(monkeypatch):
    calls = []
    fake_process = object()

    def fake_popen(cmd, cwd):
        calls.append((cmd, cwd))
        return fake_process

    monkeypatch.setattr(gopennamu_process.subprocess, "Popen", fake_popen)

    process = gopennamu_process.start_gopennamu_process(
        bin_dir="/wiki/bin",
        executable_name="main.amd64.bin",
        golang_port="3001",
        run_mode="dev",
    )

    assert process is fake_process
    assert calls == [(["/wiki/bin/main.amd64.bin", "3001", "dev", "api"], "/wiki/bin")]


def test_terminate_gopennamu_process는_timeout이면_kill을_시도한다():
    process = FakeProcess()

    gopennamu_process.terminate_gopennamu_process(process)

    assert process.terminated is True
    assert process.killed is True
    assert process.wait_calls == 2
