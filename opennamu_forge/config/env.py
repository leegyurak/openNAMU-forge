from __future__ import annotations

import os
from collections.abc import Mapping
from pathlib import Path


def parse_env_line(line: str) -> tuple[str, str] | None:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None

    if stripped.startswith("export "):
        stripped = stripped[7:].strip()

    if "=" not in stripped:
        return None

    key, value = stripped.split("=", 1)
    key = key.strip()
    value = value.strip()
    if not key:
        return None

    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    else:
        value = value.split(" #", 1)[0].strip()

    return key, value


def load_env_file(path: str | os.PathLike[str] = ".env", *, override: bool = False) -> bool:
    env_path = Path(path)
    if not env_path.exists():
        return False

    for line in env_path.read_text(encoding="utf-8").splitlines():
        parsed = parse_env_line(line)
        if parsed is None:
            continue

        key, value = parsed
        if override or key not in os.environ:
            os.environ[key] = value

    return True


def env_bool(environ: Mapping[str, str], key: str, *, default: bool) -> bool:
    raw_value = environ.get(key)
    if raw_value is None:
        return default

    normalized = raw_value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False

    return default
