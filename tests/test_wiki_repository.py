from pathlib import Path

import pytest


@pytest.fixture()
def seeded_wiki_db_set(tmp_path):
    from opennamu_forge.infrastructure.database_engine import reset_sqlmodel_engine
    from opennamu_forge.infrastructure.db_model import Backlink, WikiData, get_sqlmodel_session
    from opennamu_forge.infrastructure.migrations import run_schema_migrations

    db_set = {"type": "sqlite", "name": str(Path(tmp_path) / "wiki")}
    reset_sqlmodel_engine()
    migration_result = run_schema_migrations(db_set)

    with get_sqlmodel_session(db_set) as session:
        session.add(WikiData(title="FrontPage", data="main", type=""))
        session.add(WikiData(title="user:Alpha", data="user", type=""))
        session.add(WikiData(title="file:Logo.png", data="file", type=""))
        session.add(WikiData(title="category:Docs", data="category", type=""))
        session.add(Backlink(title="FrontPage", link="LinkedPage", type="include", data=""))
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

    assert repository.count_all_titles() == 4
    assert repository.count_titles(prefix="file:") == 1
    assert repository.exists_title_prefix("file:") is True
    assert repository.exists_title_prefix("missing/") is False


def test_wiki_document_repository는_문서본문을_조회한다(seeded_wiki_db_set):
    from opennamu_forge.infrastructure.wiki_repository import WikiDocumentRepository

    repository = WikiDocumentRepository(seeded_wiki_db_set)

    assert repository.get_data("FrontPage") == "main"
    assert repository.get_data("Missing", default="fallback") == "fallback"
    assert repository.find_title("FrontPage") == "FrontPage"
    assert repository.find_title("frontpage") is None
    assert repository.find_title_case_insensitive("frontpage") == "FrontPage"


def test_wiki_document_repository는_문서를_upsert한다(seeded_wiki_db_set):
    from opennamu_forge.infrastructure.wiki_repository import WikiDocumentRepository

    repository = WikiDocumentRepository(seeded_wiki_db_set)

    repository.upsert_title("FrontPage", "updated")
    repository.upsert_title("NewPage", "created")

    assert repository.get_data("FrontPage") == "updated"
    assert repository.get_data("NewPage") == "created"


def test_wiki_document_repository는_문서제목을_변경한다(seeded_wiki_db_set):
    from opennamu_forge.infrastructure.wiki_repository import WikiDocumentRepository

    repository = WikiDocumentRepository(seeded_wiki_db_set)

    repository.rename_title("FrontPage", "MovedPage")

    assert repository.exists_title("FrontPage") is False
    assert repository.exists_title("MovedPage") is True


def test_wiki_document_repository는_문서를_삭제한다(seeded_wiki_db_set):
    from opennamu_forge.infrastructure.wiki_repository import WikiDocumentRepository

    repository = WikiDocumentRepository(seeded_wiki_db_set)

    repository.delete_title("FrontPage")

    assert repository.exists_title("FrontPage") is False


def test_wiki_document_repository는_필요한_문서목록을_조회한다(seeded_wiki_db_set):
    from opennamu_forge.infrastructure.db_model import Backlink, get_sqlmodel_session
    from opennamu_forge.infrastructure.wiki_repository import WikiDocumentRepository

    with get_sqlmodel_session(seeded_wiki_db_set) as session:
        session.add(Backlink(title="MissingPage", link="FrontPage", type="no", data=""))
        session.commit()

    repository = WikiDocumentRepository(seeded_wiki_db_set)

    assert repository.list_needed_titles() == ["MissingPage"]


def test_wiki_document_repository는_역링크를_이동한다(seeded_wiki_db_set):
    from opennamu_forge.infrastructure.db_model import Backlink, get_sqlmodel_session
    from opennamu_forge.infrastructure.wiki_repository import WikiDocumentRepository

    repository = WikiDocumentRepository(seeded_wiki_db_set)

    repository.rename_backlink_link("LinkedPage", "MovedPage")

    with get_sqlmodel_session(seeded_wiki_db_set) as session:
        backlink = session.get(Backlink, ("FrontPage", "MovedPage", "include"))

    assert backlink is not None


def test_wiki_document_repository는_no_역링크를_추가하고_삭제한다(seeded_wiki_db_set):
    from opennamu_forge.infrastructure.db_model import Backlink, get_sqlmodel_session
    from opennamu_forge.infrastructure.wiki_repository import WikiDocumentRepository

    repository = WikiDocumentRepository(seeded_wiki_db_set)

    repository.insert_no_backlinks_for_title("FrontPage")

    with get_sqlmodel_session(seeded_wiki_db_set) as session:
        backlink = session.get(Backlink, ("FrontPage", "LinkedPage", "no"))

    assert backlink is not None

    repository.delete_no_backlinks_for_title("FrontPage")

    with get_sqlmodel_session(seeded_wiki_db_set) as session:
        backlink = session.get(Backlink, ("FrontPage", "LinkedPage", "no"))

    assert backlink is None
