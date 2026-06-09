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


def test_user_setting_repository는_name으로_id_data를_조회하고_특정_data를_제외한다(user_setting_db_set):
    from opennamu_forge.infrastructure.user_setting_repository import UserSettingRepository

    repository = UserSettingRepository(user_setting_db_set)

    repository.upsert("alpha", "acl", "admin")
    repository.upsert("beta", "acl", "user")

    rows = repository.list_id_data_by_name_excluding_data("acl", "user")

    assert len(rows) == 1
    assert rows[0] == ("alpha", "admin")


def test_user_setting_repository는_name으로_id_data를_data_역순_조회한다(user_setting_db_set):
    from opennamu_forge.infrastructure.user_setting_repository import UserSettingRepository

    repository = UserSettingRepository(user_setting_db_set)

    repository.upsert("alpha", "date", "2026-01-01")
    repository.upsert("beta", "date", "2026-01-02")

    rows = repository.list_id_data_by_name_ordered_by_data_desc("date")

    assert len(rows) == 2
    assert rows[0] == ("beta", "2026-01-02")
    assert rows[1] == ("alpha", "2026-01-01")


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


def test_user_setting_repository는_setting_존재를_확인한다(user_setting_db_set):
    from opennamu_forge.infrastructure.user_setting_repository import UserSettingRepository

    repository = UserSettingRepository(user_setting_db_set)

    repository.upsert("tester", "challenge_admin", "")

    assert repository.exists("tester", "challenge_admin") is True
    assert repository.exists("tester", "missing") is False


def test_user_setting_repository는_id_존재와_전체_존재를_확인한다(user_setting_db_set):
    from opennamu_forge.infrastructure.user_setting_repository import UserSettingRepository

    repository = UserSettingRepository(user_setting_db_set)

    assert repository.has_any() is False
    assert repository.id_exists("tester") is False

    repository.upsert("tester", "pw", "hash")

    assert repository.has_any() is True
    assert repository.id_exists("tester") is True


def test_user_setting_repository는_data까지_존재를_확인한다(user_setting_db_set):
    from opennamu_forge.infrastructure.user_setting_repository import UserSettingRepository

    repository = UserSettingRepository(user_setting_db_set)

    repository.upsert("tester", "watchlist", "FrontPage")

    assert repository.exists_data("tester", "watchlist", "FrontPage") is True
    assert repository.exists_data("tester", "watchlist", "Missing") is False


def test_user_setting_repository는_name과_data로_존재를_확인한다(user_setting_db_set):
    from opennamu_forge.infrastructure.user_setting_repository import UserSettingRepository

    repository = UserSettingRepository(user_setting_db_set)

    repository.upsert("tester", "random_key", "key-value")

    assert repository.data_exists("random_key", "key-value") is True
    assert repository.data_exists("random_key", "missing") is False
    assert repository.user_data_exists("tester", "key-value") is True
    assert repository.user_data_exists("tester", "missing") is False


def test_user_setting_repository는_name과_data로_id를_조회한다(user_setting_db_set):
    from opennamu_forge.infrastructure.user_setting_repository import UserSettingRepository

    repository = UserSettingRepository(user_setting_db_set)

    repository.upsert("tester", "random_key", "key-value")

    assert repository.find_id_by_name_data("random_key", "key-value") == "tester"
    assert repository.find_id_by_name_data("random_key", "missing") is None


def test_user_setting_repository는_name과_data로_id_목록을_조회한다(user_setting_db_set):
    from opennamu_forge.infrastructure.user_setting_repository import UserSettingRepository

    repository = UserSettingRepository(user_setting_db_set)

    repository.upsert("alpha", "watchlist", "FrontPage")
    repository.upsert("beta", "watchlist", "FrontPage")

    assert sorted(repository.list_ids_by_name_data("watchlist", "FrontPage")) == ["alpha", "beta"]


def test_user_setting_repository는_name별_count를_조회한다(user_setting_db_set):
    from opennamu_forge.infrastructure.user_setting_repository import UserSettingRepository

    repository = UserSettingRepository(user_setting_db_set)

    repository.upsert("tester", "watchlist", "FrontPage")
    repository.upsert("tester", "star_doc", "FrontPage")

    assert repository.count_by_name("tester", "watchlist") == 1
    assert repository.count_by_name("tester", "star_doc") == 1
    assert repository.count_by_name("missing", "watchlist") == 0


def test_user_setting_repository는_data까지_지정해_삭제한다(user_setting_db_set):
    from opennamu_forge.infrastructure.user_setting_repository import UserSettingRepository

    repository = UserSettingRepository(user_setting_db_set)

    repository.upsert("tester", "watchlist", "FrontPage")
    repository.upsert("tester", "star_doc", "FrontPage")
    repository.delete_data("tester", "watchlist", "FrontPage")

    assert repository.exists_data("tester", "watchlist", "FrontPage") is False
    assert repository.exists_data("tester", "star_doc", "FrontPage") is True
