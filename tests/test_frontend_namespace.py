import re
from itertools import chain
from pathlib import Path

import pytest

SKIPPED_SUFFIXES = frozenset({".png", ".webp", ".ico", ".svg"})
SKIPPED_PARTS = frozenset({"__pycache__"})
FRONTEND_NAMESPACE_FILES = tuple(
    filter(
        lambda file_path: (
            file_path.is_file()
            and file_path.suffix not in SKIPPED_SUFFIXES
            and SKIPPED_PARTS.isdisjoint(file_path.parts)
        ),
        chain((Path("app.py"),), Path("opennamu_forge/presentation/routes").rglob("*"), Path("views").rglob("*")),
    )
)


LEGACY_PATTERN = re.compile(r"opennamu_(?!forge)")
DOUBLED_PATTERN = re.compile(r"opennamu_forge_forge")


@pytest.mark.parametrize("file_path", FRONTEND_NAMESPACE_FILES, ids=str)
def test_frontend_namespace는_forge_prefix만_사용한다(file_path):
    text = file_path.read_text(encoding="utf-8", errors="ignore")
    assert LEGACY_PATTERN.search(text) is None
    assert DOUBLED_PATTERN.search(text) is None
