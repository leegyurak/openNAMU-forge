from __future__ import annotations

from collections.abc import Callable


def normalize_recent_documents(raw_recent_documents) -> list[str]:
    return raw_recent_documents if isinstance(raw_recent_documents, list) else []


def find_last_redirect_source(recent_documents: list[str], redirect_exists: Callable[[str], bool]) -> str:
    last_page = ""

    for document_name in reversed(recent_documents):
        last_page = document_name
        if redirect_exists(last_page):
            break

    return last_page


def remember_recent_document(recent_documents: list[str], name: str) -> list[str]:
    if len(recent_documents) >= 10:
        next_documents = recent_documents[-9:] + [name]
    else:
        next_documents = recent_documents + [name]

    return list(reversed(dict.fromkeys(reversed(next_documents))))
