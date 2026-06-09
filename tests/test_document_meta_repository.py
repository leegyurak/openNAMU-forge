from pathlib import Path

import pytest


@pytest.fixture()
def seeded_document_meta_db_set(tmp_path):
    from opennamu_forge.infrastructure.database_engine import reset_sqlmodel_engine
    from opennamu_forge.infrastructure.db_model import Acl, DataSet, get_sqlmodel_session
    from opennamu_forge.infrastructure.migrations import run_schema_migrations

    db_set = {"type": "sqlite", "name": str(Path(tmp_path) / "document-meta")}
    reset_sqlmodel_engine()
    migration_result = run_schema_migrations(db_set)

    with get_sqlmodel_session(db_set) as session:
        session.add(DataSet(doc_name="NoLink", doc_rev="", set_name="link_count", set_data="0"))
        session.add(DataSet(doc_name="HasLink", doc_rev="", set_name="link_count", set_data="1"))
        session.add(DataSet(doc_name="NoLink", doc_rev="", set_name="doc_type", set_data="normal"))
        session.add(DataSet(doc_name="OldNoLink", doc_rev="1", set_name="link_count", set_data="0"))
        session.add(Acl(title="NoLink", type="view", data=""))
        session.commit()

    yield db_set

    migration_result.engine.dispose()
    reset_sqlmodel_engine()


def test_document_meta_repository는_meta를_조회한다(seeded_document_meta_db_set):
    from opennamu_forge.infrastructure.document_meta_repository import DocumentMetaRepository

    repository = DocumentMetaRepository(seeded_document_meta_db_set)

    assert repository.get("NoLink", "doc_type") == "normal"


def test_document_meta_repository는_없는_meta에_기본값을_반환한다(seeded_document_meta_db_set):
    from opennamu_forge.infrastructure.document_meta_repository import DocumentMetaRepository

    repository = DocumentMetaRepository(seeded_document_meta_db_set)

    assert repository.get("Missing", "doc_type", default="fallback") == "fallback"


def test_document_meta_repository는_meta_존재를_확인한다(seeded_document_meta_db_set):
    from opennamu_forge.infrastructure.document_meta_repository import DocumentMetaRepository

    repository = DocumentMetaRepository(seeded_document_meta_db_set)

    assert repository.exists("NoLink", "doc_type") is True
    assert repository.exists("Missing", "doc_type") is False


def test_document_meta_repository는_no_link_문서만_조회한다(seeded_document_meta_db_set):
    from opennamu_forge.infrastructure.document_meta_repository import DocumentMetaRepository

    repository = DocumentMetaRepository(seeded_document_meta_db_set)

    assert repository.list_no_link_documents() == [("NoLink", "0")]


def test_document_meta_repository는_meta를_upsert하고_삭제한다(seeded_document_meta_db_set):
    from opennamu_forge.infrastructure.document_meta_repository import DocumentMetaRepository

    repository = DocumentMetaRepository(seeded_document_meta_db_set)

    repository.upsert("NoLink", "document_top", "top")
    repository.upsert("NoLink", "document_top", "moved")

    assert repository.get("NoLink", "document_top") == "moved"

    repository.delete("NoLink", "document_top")

    assert repository.get("NoLink", "document_top") == ""


def test_document_meta_repository는_revision_marker를_변경한다(seeded_document_meta_db_set):
    from opennamu_forge.infrastructure.document_meta_repository import DocumentMetaRepository

    repository = DocumentMetaRepository(seeded_document_meta_db_set)

    repository.upsert("NoLink", "length", "10")
    repository.update_revision_marker("NoLink", "not_exist")

    assert repository.get("NoLink", "length", doc_rev="not_exist") == "10"


def test_document_meta_repository는_acl을_조회하고_upsert한다(seeded_document_meta_db_set):
    from opennamu_forge.infrastructure.document_meta_repository import DocumentMetaRepository

    repository = DocumentMetaRepository(seeded_document_meta_db_set)

    repository.upsert_acl("FrontPage", "view", "admin")
    repository.upsert_acl("FrontPage", "why", "reason")
    repository.upsert_acl("user:Alpha", "view", "admin")

    acl_entries = repository.list_acl_entries()

    assert repository.get_acl("FrontPage", "view") == "admin"
    assert repository.acl_title_exists("FrontPage") is True
    assert len(acl_entries) == 2
    assert acl_entries[0].title == "FrontPage"


def test_document_meta_repository는_doc_name을_변경한다(seeded_document_meta_db_set):
    from opennamu_forge.infrastructure.document_meta_repository import DocumentMetaRepository

    repository = DocumentMetaRepository(seeded_document_meta_db_set)

    repository.rename_doc_name("NoLink", "MovedNoLink")

    assert repository.get("MovedNoLink", "doc_type") == "normal"


def test_document_meta_repository는_doc_name을_삭제한다(seeded_document_meta_db_set):
    from opennamu_forge.infrastructure.document_meta_repository import DocumentMetaRepository

    repository = DocumentMetaRepository(seeded_document_meta_db_set)

    repository.delete_doc_name("NoLink")

    assert repository.get("NoLink", "doc_type", default="fallback") == "fallback"


def test_document_meta_repository는_acl_title을_변경하고_삭제한다(seeded_document_meta_db_set):
    from opennamu_forge.infrastructure.db_model import Acl, get_sqlmodel_session
    from opennamu_forge.infrastructure.document_meta_repository import DocumentMetaRepository

    repository = DocumentMetaRepository(seeded_document_meta_db_set)

    repository.rename_acl_title("NoLink", "MovedNoLink")

    with get_sqlmodel_session(seeded_document_meta_db_set) as session:
        acl = session.get(Acl, ("MovedNoLink", "view"))

    assert acl is not None

    repository.delete_acl_title("MovedNoLink")

    with get_sqlmodel_session(seeded_document_meta_db_set) as session:
        acl = session.get(Acl, ("MovedNoLink", "view"))

    assert acl is None
