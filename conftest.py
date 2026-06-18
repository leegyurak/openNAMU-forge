from __future__ import annotations

import shutil

import pytest


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if shutil.which("rg") is not None:
        return

    skip_marker = pytest.mark.skip(reason="ripgrep(rg) binary not found on PATH")
    for item in items:
        if "requires_ripgrep" in item.keywords:
            item.add_marker(skip_marker)
