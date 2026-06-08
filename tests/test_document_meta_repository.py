from pathlib import Path

import pytest


@pytest.fixture()
def seeded_document_meta_db_set(tmp_path):
    from opennamu_forge.infrastructure.database_config import reset_sqlmodel_engine
    from opennamu_forge.infrastructure.db_model import DataSet, get_sqlmodel_session
    from opennamu_forge.infrastructure.migrations import run_schema_migrations

    db_set = {"type": "sqlite", "name": str(Path(tmp_path) / "document-meta")}
    reset_sqlmodel_engine()
    migration_result = run_schema_migrations(db_set)

    with get_sqlmodel_session(db_set) as session:
        session.add(DataSet(doc_name="NoLink", doc_rev="", set_name="link_count", set_data="0"))
        session.add(DataSet(doc_name="HasLink", doc_rev="", set_name="link_count", set_data="1"))
        session.add(DataSet(doc_name="NoLink", doc_rev="", set_name="doc_type", set_data="normal"))
        session.add(DataSet(doc_name="OldNoLink", doc_rev="1", set_name="link_count", set_data="0"))
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


def test_document_meta_repository는_no_link_문서만_조회한다(seeded_document_meta_db_set):
    from opennamu_forge.infrastructure.document_meta_repository import DocumentMetaRepository

    repository = DocumentMetaRepository(seeded_document_meta_db_set)

    assert repository.list_no_link_documents() == [("NoLink", "0")]
