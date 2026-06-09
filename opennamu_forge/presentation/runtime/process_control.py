from __future__ import annotations

import os
import subprocess
import sys
import threading
import time
from collections.abc import Callable, Sequence

from opennamu_forge.infrastructure.logging import get_logger

logger = get_logger(__name__)


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
