from pathlib import Path

import pytest


@pytest.fixture()
def user_setting_db_set(tmp_path):
    from opennamu_forge.infrastructure.database_config import reset_sqlmodel_engine
    from opennamu_forge.infrastructure.migrations import run_schema_migrations

    db_set = {"type": "sqlite", "name": str(Path(tmp_path) / "user-setting")}
    reset_sqlmodel_engine()
    migration_result = run_schema_migrations(db_set)

    yield db_set

    migration_result.engine.dispose()
    reset_sqlmodel_engine()


def test_user_setting_repository는_setting을_upsert한다(user_setting_db_set):
    from opennamu_forge.infrastructure.user_setting_repository import UserSettingRepository

    repository = UserSettingRepository(user_setting_db_set)

    repository.upsert("tester", "lang", "ko")
    repository.upsert("tester", "lang", "en")

    assert repository.get("tester", "lang") == "en"


def test_user_setting_repository는_name으로_data를_조회한다(user_setting_db_set):
    from opennamu_forge.infrastructure.user_setting_repository import UserSettingRepository

    repository = UserSettingRepository(user_setting_db_set)

    repository.upsert("alpha", "application", "one")
    repository.upsert("beta", "application", "two")

    assert sorted(repository.list_data_by_name("application")) == ["one", "two"]


def test_user_setting_repository는_setting을_삭제한다(user_setting_db_set):
    from opennamu_forge.infrastructure.user_setting_repository import UserSettingRepository

    repository = UserSettingRepository(user_setting_db_set)

    repository.upsert("tester", "application", "payload")
    repository.delete("tester", "application")

    assert repository.get("tester", "application") == ""


def test_user_setting_repository는_없는_setting에_기본값을_반환한다(user_setting_db_set):
    from opennamu_forge.infrastructure.user_setting_repository import UserSettingRepository

    repository = UserSettingRepository(user_setting_db_set)

    assert repository.get("tester", "missing", default="fallback") == "fallback"
