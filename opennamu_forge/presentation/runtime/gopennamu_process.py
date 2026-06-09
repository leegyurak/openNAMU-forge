from __future__ import annotations

import asyncio
import subprocess
import time
from collections.abc import Mapping
from pathlib import Path
from typing import Protocol

import psutil
import requests

from opennamu_forge.infrastructure.logging import get_logger
from opennamu_forge.presentation.encoding_helpers import json_dumps

logger = get_logger(__name__)

class GopenNamuProcess(Protocol):
    def poll(self): ...

    def terminate(self) -> None: ...

    def kill(self) -> None: ...

    def wait(self, timeout: float | None = None): ...

async def wait_for_gopennamu(database_runtime_options: Mapping[str, str], golang_port: str) -> None:
    while True:
        try:
            db_payload = {("db_" + key): value for key, value in database_runtime_options.items()}
            payload = {
                "url": "test",
                "data": json_dumps(db_payload),
                "session": "{}",
                "cookies": "",
                "ip": "127.0.0.1",
            }

            response = requests.post(
                "http://127.0.0.1:" + golang_port + "/compatible_api/test",
                data=json_dumps(payload),
            )
            if response.status_code == 200:
                logger.info("Golang turn on")
                break
        except requests.ConnectionError:
            logger.info("Wait golang...")
            time.sleep(1)

def kill_port(port: str | int, timeout: float = 1.5, force: bool = True) -> list[int]:
    pids = {
        c.pid
        for c in psutil.net_connections(kind="inet")
        if c.pid and c.laddr and c.laddr.port == int(port) and c.status == psutil.CONN_LISTEN
    }
    procs = []
    for pid in pids:
        try:
            process = psutil.Process(pid)
            process.terminate()
            procs.append(process)
        except psutil.NoSuchProcess:
            pass
        except psutil.AccessDenied:
            logger.exception("Golang PID is not dying, please shut down manually by sudo.")
            raise

    _, alive = psutil.wait_procs(procs, timeout=timeout)
    if force:
        for process in alive:
            try:
                process.kill()
            except psutil.NoSuchProcess:
                pass
            except psutil.AccessDenied:
                logger.exception("Golang PID is not dying, please shut down manually by sudo.")
                raise

        psutil.wait_procs(alive, timeout=timeout)

    return sorted(pids)

def start_gopennamu_process(
    *,
    bin_dir: str | Path,
    executable_name: str,
    golang_port: str,
    run_mode: str,
) -> subprocess.Popen:
    exe_path = Path(bin_dir) / executable_name
    cmd = [str(exe_path), golang_port, run_mode, "api"]
    return subprocess.Popen(cmd, cwd=str(bin_dir))

def wait_for_gopennamu_startup(database_runtime_options: Mapping[str, str], golang_port: str) -> None:
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(wait_for_gopennamu(database_runtime_options, golang_port))
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(wait_for_gopennamu(database_runtime_options, golang_port))

def terminate_gopennamu_process(golang_process: GopenNamuProcess) -> None:
    if golang_process.poll() is None:
        golang_process.terminate()
        try:
            golang_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            golang_process.kill()
            try:
                golang_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                logger.error("Golang process not terminated properly.")
