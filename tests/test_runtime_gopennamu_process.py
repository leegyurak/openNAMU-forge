import asyncio
import subprocess
from types import SimpleNamespace

from opennamu_forge.presentation.runtime import gopennamu_process


class FakeProcess:
    def __init__(self, poll_result=None):
        self.terminated = False
        self.killed = False
        self.wait_calls = 0
        self.poll_result = poll_result

    def terminate(self):
        self.terminated = True

    def kill(self):
        self.killed = True

    def poll(self):
        return self.poll_result

    def wait(self, timeout=None):
        self.wait_calls += 1
        if self.wait_calls == 1:
            raise subprocess.TimeoutExpired("main.bin", float(timeout or 0))
        return 0


class FakeProcessWithConnections:
    def __init__(self, pid, connections=(), access_denied=False):
        self.pid = pid
        self.connections = connections
        self.access_denied = access_denied

    def net_connections(self, kind):
        if self.access_denied:
            raise gopennamu_process.psutil.AccessDenied(pid=self.pid)

        return self.connections


def test_wait_for_gopennamu는_connection_error_후_200이면_종료한다(monkeypatch):
    calls = []

    def fake_post(url, data):
        calls.append((url, data))
        if len(calls) == 1:
            raise gopennamu_process.requests.ConnectionError()
        return SimpleNamespace(status_code=200)

    monkeypatch.setattr(gopennamu_process.requests, "post", fake_post)
    monkeypatch.setattr(gopennamu_process.time, "sleep", lambda seconds: None)

    asyncio.run(gopennamu_process.wait_for_gopennamu({"type": "sqlite", "name": "wiki"}, "3001"))

    assert calls[0][0] == "http://127.0.0.1:3001/compatible_api/test"
    assert calls[1][0] == "http://127.0.0.1:3001/compatible_api/test"
    assert '\\"db_type\\":\\"sqlite\\"' in calls[1][1]
    assert '\\"db_name\\":\\"wiki\\"' in calls[1][1]


def test_wait_for_gopennamu_startup은_running_loop가_없으면_완료까지_기다린다(monkeypatch):
    calls = []

    async def fake_wait_for_gopennamu(database_runtime_options, golang_port):
        calls.append((database_runtime_options, golang_port))

    monkeypatch.setattr(gopennamu_process, "wait_for_gopennamu", fake_wait_for_gopennamu)

    gopennamu_process.wait_for_gopennamu_startup({"type": "sqlite", "name": "wiki"}, "3001")

    assert calls == [({"type": "sqlite", "name": "wiki"}, "3001")]


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


def test_kill_port는_macos_전역_connection_권한오류시_process별_scan으로_fallback한다(monkeypatch):
    process = FakeProcess()
    connection = SimpleNamespace(laddr=SimpleNamespace(port=3001), status="LISTEN")
    inaccessible = FakeProcessWithConnections(10, access_denied=True)
    matching = FakeProcessWithConnections(20, connections=(connection,))
    other = FakeProcessWithConnections(30, connections=(SimpleNamespace(laddr=SimpleNamespace(port=3002), status="LISTEN"),))

    def fake_net_connections(kind):
        raise gopennamu_process.psutil.AccessDenied(pid=28762)

    monkeypatch.setattr(gopennamu_process.psutil, "CONN_LISTEN", "LISTEN")
    monkeypatch.setattr(gopennamu_process.psutil, "net_connections", fake_net_connections)
    monkeypatch.setattr(gopennamu_process.psutil, "process_iter", lambda attrs: (inaccessible, matching, other))
    monkeypatch.setattr(gopennamu_process.psutil, "Process", lambda pid: process)
    monkeypatch.setattr(gopennamu_process.psutil, "wait_procs", lambda procs, timeout: ((), ()))

    killed = gopennamu_process.kill_port("3001")

    assert killed == [20]
    assert process.terminated is True
    assert process.killed is False


def test_kill_port는_force_false면_alive_process를_kill하지_않는다(monkeypatch):
    process = FakeProcess()
    connection = SimpleNamespace(pid=20, laddr=SimpleNamespace(port=3001), status="LISTEN")
    monkeypatch.setattr(gopennamu_process.psutil, "CONN_LISTEN", "LISTEN")
    monkeypatch.setattr(gopennamu_process.psutil, "net_connections", lambda kind: (connection,))
    monkeypatch.setattr(gopennamu_process.psutil, "Process", lambda pid: process)
    monkeypatch.setattr(gopennamu_process.psutil, "wait_procs", lambda procs, timeout: ((), (process,)))

    killed = gopennamu_process.kill_port("3001", force=False)

    assert killed == [20]
    assert process.terminated is True
    assert process.killed is False


def test_kill_port는_no_such_process를_무시한다(monkeypatch):
    connection = SimpleNamespace(pid=20, laddr=SimpleNamespace(port=3001), status="LISTEN")

    def fake_process(pid):
        raise gopennamu_process.psutil.NoSuchProcess(pid=pid)

    monkeypatch.setattr(gopennamu_process.psutil, "CONN_LISTEN", "LISTEN")
    monkeypatch.setattr(gopennamu_process.psutil, "net_connections", lambda kind: (connection,))
    monkeypatch.setattr(gopennamu_process.psutil, "Process", fake_process)
    monkeypatch.setattr(gopennamu_process.psutil, "wait_procs", lambda procs, timeout: ((), ()))

    killed = gopennamu_process.kill_port("3001")

    assert killed == [20]


def test_start_gopennamu_process는_기존_인자를_그대로_전달한다(monkeypatch):
    calls = []
    fake_process = object()

    def fake_popen(cmd, cwd, env):
        calls.append((cmd, cwd, env["NAMU_DB_TYPE"], env["NAMU_DB"]))
        return fake_process

    monkeypatch.setattr(gopennamu_process.subprocess, "Popen", fake_popen)

    process = gopennamu_process.start_gopennamu_process(
        bin_dir="/wiki/bin",
        executable_name="main.amd64.bin",
        golang_port="3001",
        run_mode="dev",
        database_runtime_options={"type": "sqlite", "name": "data"},
    )

    assert process is fake_process
    assert calls == [(["/wiki/bin/main.amd64.bin", "3001", "dev", "api"], "/wiki/bin", "sqlite", "data")]


def test_build_gopennamu_environment는_mysql_설정을_env로_전달한다(monkeypatch):
    monkeypatch.setattr(gopennamu_process.os, "environ", {"PATH": "/bin"})

    env = gopennamu_process.build_gopennamu_environment(
        {
            "type": "mysql",
            "name": "wiki",
            "mysql_host": "db",
            "mysql_port": "3307",
            "mysql_user": "user",
            "mysql_pw": "pw",
        }
    )

    assert env == {
        "PATH": "/bin",
        "NAMU_DB_TYPE": "mysql",
        "NAMU_DB": "wiki",
        "NAMU_DB_HOST": "db",
        "NAMU_DB_PORT": "3307",
        "NAMU_DB_USER": "user",
        "NAMU_DB_PASSWORD": "pw",
    }


def test_build_gopennamu_environment는_postgresql_설정을_env로_전달한다(monkeypatch):
    monkeypatch.setattr(gopennamu_process.os, "environ", {"PATH": "/bin"})

    env = gopennamu_process.build_gopennamu_environment(
        {
            "type": "postgresql",
            "name": "wiki",
            "postgresql_host": "db",
            "postgresql_port": "5433",
            "postgresql_user": "user",
            "postgresql_pw": "pw",
        }
    )

    assert env == {
        "PATH": "/bin",
        "NAMU_DB_TYPE": "postgresql",
        "NAMU_DB": "wiki",
        "NAMU_DB_HOST": "db",
        "NAMU_DB_PORT": "5433",
        "NAMU_DB_USER": "user",
        "NAMU_DB_PASSWORD": "pw",
    }


def test_terminate_gopennamu_process는_timeout이면_kill을_시도한다():
    process = FakeProcess()

    gopennamu_process.terminate_gopennamu_process(process)

    assert process.terminated is True
    assert process.killed is True
    assert process.wait_calls == 2


def test_terminate_gopennamu_process는_이미_종료된_process를_건드리지_않는다():
    process = FakeProcess(poll_result=0)

    gopennamu_process.terminate_gopennamu_process(process)

    assert process.terminated is False
    assert process.killed is False
    assert process.wait_calls == 0
