from opennamu_forge.presentation.view_session_helpers import (
    find_last_redirect_source,
    normalize_recent_documents,
    remember_recent_document,
)


def test_normalize_recent_documents는_list만_통과시킨다():
    assert normalize_recent_documents(["A"]) == ["A"]
    assert normalize_recent_documents("A") == []


def test_remember_recent_document는_최근_문서_중복을_제거하고_10개로_제한한다():
    recent_documents = ["A", "B", "A", "C", "D", "E", "F", "G", "H", "I"]

    assert remember_recent_document(recent_documents, "J") == ["B", "A", "C", "D", "E", "F", "G", "H", "I", "J"]


def test_find_last_redirect_source는_가장_최근_redirect_source를_반환한다():
    assert find_last_redirect_source(["A", "B", "C"], lambda name: name == "B") == "B"
