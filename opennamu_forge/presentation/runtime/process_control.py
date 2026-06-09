from __future__ import annotations

import atexit
import os
import signal
import subprocess
import sys
import threading
import time
from collections.abc import Callable, Sequence
from types import FrameType
from typing import TypeVar

from opennamu_forge.infrastructure.logging import get_logger

logger = get_logger(__name__)
ProcessT = TypeVar("ProcessT")


def build_python_restart_candidates(
    executable: str = sys.executable,
    major: int = sys.version_info.major,
    minor: int = sys.version_info.minor,
) -> tuple[str, ...]:
    python_version = f"{major}.{minor}"
    return (
        executable,
        f"python{python_version}",
        "python3",
        "python",
        f"py -{python_version}",
    )


def restart_current_process(
    argv: Sequence[str] | None = None,
    *,
    exit_process: Callable[[int], object] = os._exit,
    popen: Callable[[list[str]], object] = subprocess.Popen,
    sleep: Callable[[float], object] = time.sleep,
) -> None:
    logger.info("Restart")

    sleep(3)
    process_argv = tuple(sys.argv if argv is None else argv)

    for executable in build_python_restart_candidates():
        try:
            popen([executable, *process_argv])
            break
        except OSError:
            continue

    exit_process(0)


def schedule_restart() -> threading.Thread:
    thread = threading.Thread(target=restart_current_process, daemon=True)
    thread.start()
    return thread


def shutdown_current_process(exit_process: Callable[[], object] = sys.exit) -> None:
    logger.info("Shutdown")
    exit_process()


def register_termination_handlers(
    process: ProcessT,
    terminate_process: Callable[[ProcessT], object],
    *,
    signal_func: Callable[..., object] = signal.signal,
    atexit_register: Callable[..., object] = atexit.register,
    exit_process: Callable[[int], object] = os._exit,
) -> None:
    def signal_handler(signal_number: int, frame: FrameType | None) -> None:
        logger.info("EXIT SIGNAL RECEIVED")
        terminate_process(process)
        exit_process(0)

    signal_func(signal.SIGTERM, signal_handler)
    signal_func(signal.SIGINT, signal_handler)
    atexit_register(terminate_process, process)
