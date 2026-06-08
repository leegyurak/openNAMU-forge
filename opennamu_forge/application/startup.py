from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeSettings:
    run_mode: str
    host: str
    port: str
    golang_port: str


def normalize_run_mode(raw_mode: str) -> str:
    return raw_mode if raw_mode == "dev" else ""
