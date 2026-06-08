from __future__ import annotations

import importlib
import sys
from types import ModuleType

from flask import Flask

_runtime_app_module: ModuleType | None = None


def load_runtime_app() -> ModuleType:
    global _runtime_app_module

    if _runtime_app_module is None:
        _runtime_app_module = importlib.import_module("opennamu_forge.presentation.runtime_app")

    return _runtime_app_module


def create_app() -> Flask:
    return load_runtime_app().app


def main() -> None:
    runtime_app = load_runtime_app()
    runtime_app.run_app()


if __name__ == "__main__":
    sys.exit(main())
