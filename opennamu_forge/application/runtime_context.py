from __future__ import annotations

from typing import Any

_runtime_values: dict[str, Any] = {}


def set_runtime_value(name: str, value: Any) -> Any:
    _runtime_values[name] = value
    return value


def get_runtime_value(name: str, default: Any = None) -> Any:
    return _runtime_values.get(name, default)


def clear_runtime_context() -> None:
    _runtime_values.clear()
