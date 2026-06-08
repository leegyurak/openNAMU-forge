from pathlib import Path

import pytest


@pytest.fixture()
def seeded_wiki_db_set(tmp_path):
    from opennamu_forge.infrastructure.database_config import reset_sqlmodel_engine
    from opennamu_forge.infrastructure.db_model import WikiData, get_sqlmodel_session
    from opennamu_forge.infrastructure.migrations import run_schema_migrations

    db_set = {"type": "sqlite", "name": str(Path(tmp_path) / "wiki")}
    reset_sqlmodel_engine()
    migration_result = run_schema_migrations(db_set)

    with get_sqlmodel_session(db_set) as session:
        session.add(WikiData(title="FrontPage", data="main", type=""))
        session.add(WikiData(title="user:Alpha", data="user", type=""))
        session.add(WikiData(title="file:Logo.png", data="file", type=""))
        session.add(WikiData(title="category:Docs", data="category", type=""))
        session.commit()

    yield db_set

    migration_result.engine.dispose()
    reset_sqlmodel_engine()


def test_wiki_document_repository는_전체_title을_조회한다(seeded_wiki_db_set):
    from opennamu_forge.infrastructure.wiki_repository import WikiDocumentRepository

    repository = WikiDocumentRepository(seeded_wiki_db_set)

    assert repository.list_titles() == ["FrontPage", "category:Docs", "file:Logo.png", "user:Alpha"]


def test_wiki_document_repository는_user_page를_제외한다(seeded_wiki_db_set):
    from opennamu_forge.infrastructure.wiki_repository import WikiDocumentRepository

    repository = WikiDocumentRepository(seeded_wiki_db_set)

    assert repository.list_titles(exclude_user_pages=True) == ["FrontPage", "category:Docs", "file:Logo.png"]


def test_wiki_document_repository는_file_page를_제외한다(seeded_wiki_db_set):
    from opennamu_forge.infrastructure.wiki_repository import WikiDocumentRepository

    repository = WikiDocumentRepository(seeded_wiki_db_set)

    assert repository.list_titles(exclude_file_pages=True) == ["FrontPage", "category:Docs", "user:Alpha"]


def test_wiki_document_repository는_category_page를_제외한다(seeded_wiki_db_set):
    from opennamu_forge.infrastructure.wiki_repository import WikiDocumentRepository

    repository = WikiDocumentRepository(seeded_wiki_db_set)

    assert repository.list_titles(exclude_category_pages=True) == ["FrontPage", "file:Logo.png", "user:Alpha"]


def test_wiki_document_repository는_복합_exclude를_적용한다(seeded_wiki_db_set):
    from opennamu_forge.infrastructure.wiki_repository import WikiDocumentRepository

    repository = WikiDocumentRepository(seeded_wiki_db_set)

    assert repository.list_titles(
        exclude_user_pages=True,
        exclude_file_pages=True,
        exclude_category_pages=True,
    ) == ["FrontPage"]


def test_wiki_document_repository는_prefix_page를_조회한다(seeded_wiki_db_set):
    from opennamu_forge.infrastructure.wiki_repository import WikiDocumentRepository

    repository = WikiDocumentRepository(seeded_wiki_db_set)

    assert repository.list_titles_page(prefix="file:") == ["file:Logo.png"]


def test_wiki_document_repository는_offset과_limit을_적용한다(seeded_wiki_db_set):
    from opennamu_forge.infrastructure.wiki_repository import WikiDocumentRepository

    repository = WikiDocumentRepository(seeded_wiki_db_set)

    assert repository.list_titles_page(offset=1, limit=2) == ["category:Docs", "file:Logo.png"]


def test_wiki_document_repository는_prefix_count를_조회한다(seeded_wiki_db_set):
    from opennamu_forge.infrastructure.wiki_repository import WikiDocumentRepository

    repository = WikiDocumentRepository(seeded_wiki_db_set)

    assert repository.count_titles(prefix="file:") == 1
