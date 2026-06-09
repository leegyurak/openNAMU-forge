from pathlib import Path

import pytest


@pytest.fixture()
def backlink_db_set(tmp_path):
    from opennamu_forge.infrastructure.database_engine import reset_sqlmodel_engine
    from opennamu_forge.infrastructure.db_model import Backlink, get_sqlmodel_session
    from opennamu_forge.infrastructure.migrations import run_schema_migrations

    db_set = {"type": "sqlite", "name": str(Path(tmp_path) / "backlink")}
    reset_sqlmodel_engine()
    migration_result = run_schema_migrations(db_set)

    with get_sqlmodel_session(db_set) as session:
        session.add(Backlink(title="FrontPage", link="Category", type="cat", data=""))
        session.add(Backlink(title="FrontPage", link="Hidden", type="cat_blur", data=""))
        session.add(Backlink(title="FrontPage", link="Category", type="cat_view", data="Shown"))
        session.add(Backlink(title="Included", link="FrontPage", type="include", data=""))
        session.add(Backlink(title="Old", link="FrontPage", type="redirect", data="#section"))
        session.commit()

    yield db_set

    migration_result.engine.dispose()
    reset_sqlmodel_engine()


def test_backlink_repository는_distinct_ref를_조회한다(backlink_db_set):
    from opennamu_forge.infrastructure.backlink_repository import BacklinkRepository

    repository = BacklinkRepository(backlink_db_set)

    rows = repository.list_distinct_refs("title", "link", "FrontPage")
    insensitive_rows = repository.list_distinct_refs_case_insensitive("title", "link", "frontpage")

    assert rows[0] == ("Included", "include")
    assert rows[1] == ("Old", "redirect")
    assert insensitive_rows[0] == ("Included", "include")


def test_backlink_repository는_category_link와_data를_조회한다(backlink_db_set):
    from opennamu_forge.infrastructure.backlink_repository import BacklinkRepository

    repository = BacklinkRepository(backlink_db_set)

    assert repository.list_distinct_links_by_title_type("FrontPage", "cat") == ["Category"]
    assert repository.get_data("FrontPage", "Category", "cat_view") == "Shown"
    assert repository.exists("FrontPage", "Hidden", "cat_blur") is True


def test_backlink_repository는_include와_redirect를_조회한다(backlink_db_set):
    from opennamu_forge.infrastructure.backlink_repository import BacklinkRepository

    repository = BacklinkRepository(backlink_db_set)

    assert repository.has_include_title("Included") is True
    assert repository.get_redirect_for_link("FrontPage") == ("Old", "#section")
    assert repository.redirect_exists_for_title_or_link("Old") is True


def test_backlink_repository는_document_backlink를_교체한다(backlink_db_set):
    from opennamu_forge.infrastructure.backlink_repository import BacklinkRepository

    repository = BacklinkRepository(backlink_db_set)

    repository.replace_for_document("Category", [("Category", "NewPage", "link", "")])

    assert repository.exists("FrontPage", "Category", "cat") is False
    assert repository.exists("NewPage", "Category", "link") is True
