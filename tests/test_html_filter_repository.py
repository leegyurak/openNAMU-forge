from pathlib import Path

import pytest


@pytest.fixture()
def html_filter_db_set(tmp_path):
    from opennamu_forge.infrastructure.database_config import reset_sqlmodel_engine
    from opennamu_forge.infrastructure.db_model import HtmlFilter, get_sqlmodel_session
    from opennamu_forge.infrastructure.migrations import run_schema_migrations

    db_set = {"type": "sqlite", "name": str(Path(tmp_path) / "html-filter")}
    reset_sqlmodel_engine()
    migration_result = run_schema_migrations(db_set)

    with get_sqlmodel_session(db_set) as session:
        session.add(HtmlFilter(html="example.com", kind="email", plus="", plus_t=""))
        session.add(HtmlFilter(html="Template", kind="template", plus="Help", plus_t=""))
        session.add(HtmlFilter(html="rule", kind="regex_filter", plus="spam", plus_t="X"))
        session.add(HtmlFilter(html="empty", kind="regex_filter", plus="", plus_t="X"))
        session.commit()

    yield db_set

    migration_result.engine.dispose()
    reset_sqlmodel_engine()


def test_html_filter_repository는_kind별_filter를_조회한다(html_filter_db_set):
    from opennamu_forge.infrastructure.html_filter_repository import HtmlFilterRepository

    repository = HtmlFilterRepository(html_filter_db_set)

    rows = repository.list_by_kind("template")

    assert len(rows) == 1
    assert rows[0].html == "Template"
    assert rows[0].plus == "Help"


def test_html_filter_repository는_plus가_있는_regex_filter를_조회한다(html_filter_db_set):
    from opennamu_forge.infrastructure.html_filter_repository import HtmlFilterRepository

    repository = HtmlFilterRepository(html_filter_db_set)

    rows = repository.list_regex_filters_with_plus()

    assert len(rows) == 1
    assert rows[0].html == "rule"


def test_html_filter_repository는_filter_존재를_확인한다(html_filter_db_set):
    from opennamu_forge.infrastructure.html_filter_repository import HtmlFilterRepository

    repository = HtmlFilterRepository(html_filter_db_set)

    assert repository.exists("example.com", "email") is True
    assert repository.exists("missing", "email") is False


def test_html_filter_repository는_filter를_단건_조회한다(html_filter_db_set):
    from opennamu_forge.infrastructure.html_filter_repository import HtmlFilterRepository

    repository = HtmlFilterRepository(html_filter_db_set)

    row = repository.get("Template", "template")

    assert row is not None
    assert row.html == "Template"
    assert row.plus == "Help"
    assert repository.get("missing", "template") is None


def test_html_filter_repository는_kind와_plus로_filter를_조회한다(html_filter_db_set):
    from opennamu_forge.infrastructure.html_filter_repository import HtmlFilterRepository

    repository = HtmlFilterRepository(html_filter_db_set)

    row = repository.get_by_kind_plus("template", "Help")

    assert row is not None
    assert row.html == "Template"


def test_html_filter_repository는_plus_t를_조회한다(html_filter_db_set):
    from opennamu_forge.infrastructure.html_filter_repository import HtmlFilterRepository

    repository = HtmlFilterRepository(html_filter_db_set)

    assert repository.get_plus_t("rule", "regex_filter") == "X"
    assert repository.get_plus_t("missing", "regex_filter", default="fallback") == "fallback"


def test_html_filter_repository는_filter를_upsert한다(html_filter_db_set):
    from opennamu_forge.infrastructure.html_filter_repository import HtmlFilterRepository

    repository = HtmlFilterRepository(html_filter_db_set)

    repository.upsert("Template", "template", plus="Updated", plus_t="memo")
    repository.upsert("New", "template", plus="Created")

    updated = repository.get("Template", "template")
    created = repository.get("New", "template")

    assert updated is not None
    assert updated.plus == "Updated"
    assert updated.plus_t == "memo"
    assert created is not None
    assert created.plus == "Created"


def test_html_filter_repository는_filter를_삭제한다(html_filter_db_set):
    from opennamu_forge.infrastructure.html_filter_repository import HtmlFilterRepository

    repository = HtmlFilterRepository(html_filter_db_set)

    repository.delete("example.com", "email")

    assert repository.exists("example.com", "email") is False
