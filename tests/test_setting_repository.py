from pathlib import Path

import pytest


@pytest.fixture()
def sqlite_db_set(tmp_path):
    return {"type": "sqlite", "name": str(Path(tmp_path) / "settings")}


def test_other_setting_repository는_setting을_upsert한다(sqlite_db_set):
    from opennamu_forge.infrastructure.database_config import reset_sqlmodel_engine
    from opennamu_forge.infrastructure.migrations import run_schema_migrations
    from opennamu_forge.infrastructure.setting_repository import OtherSettingRepository

    reset_sqlmodel_engine()
    migration_result = run_schema_migrations(sqlite_db_set)
    repository = OtherSettingRepository(sqlite_db_set)

    repository.upsert("top_menu", "FrontPage")
    repository.upsert("top_menu", "RecentChanges")

    assert repository.get("top_menu") == "RecentChanges"
    migration_result.engine.dispose()
    reset_sqlmodel_engine()


def test_other_setting_repository는_coverage별_setting을_분리한다(sqlite_db_set):
    from opennamu_forge.infrastructure.database_config import reset_sqlmodel_engine
    from opennamu_forge.infrastructure.migrations import run_schema_migrations
    from opennamu_forge.infrastructure.setting_repository import OtherSettingRepository

    reset_sqlmodel_engine()
    migration_result = run_schema_migrations(sqlite_db_set)
    repository = OtherSettingRepository(sqlite_db_set)

    repository.upsert("head", "global")
    repository.upsert("head", "ringo", coverage="ringo")

    assert repository.get("head") == "global"
    assert repository.get("head", coverage="ringo") == "ringo"
    migration_result.engine.dispose()
    reset_sqlmodel_engine()


def test_other_setting_repository는_없는_setting을_기본값으로_반환한다(sqlite_db_set):
    from opennamu_forge.infrastructure.database_config import reset_sqlmodel_engine
    from opennamu_forge.infrastructure.migrations import run_schema_migrations
    from opennamu_forge.infrastructure.setting_repository import OtherSettingRepository

    reset_sqlmodel_engine()
    migration_result = run_schema_migrations(sqlite_db_set)
    repository = OtherSettingRepository(sqlite_db_set)

    assert repository.get("missing", default="fallback") == "fallback"
    migration_result.engine.dispose()
    reset_sqlmodel_engine()
