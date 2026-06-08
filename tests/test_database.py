import pytest

from opennamu_forge.infrastructure.database import build_database_settings_from_env, should_init_sqlmodel


@pytest.mark.parametrize("db_type", ("sqlite", "mysql", "postgresql"))
def test_sqlmodel은_지원_db에서_초기화된다(db_type):
    assert should_init_sqlmodel({"type": db_type}) is True


def test_sqlmodel_초기화_판단은_type_key를_요구한다():
    with pytest.raises(KeyError):
        should_init_sqlmodel({})


def test_env_database_settings는_postgres_alias를_정규화한다():
    db_set = build_database_settings_from_env(
        {
            "NAMU_DB_TYPE": "postgres",
            "NAMU_DB": "wiki",
            "NAMU_DB_HOST": "db",
            "NAMU_DB_PORT": "15432",
            "NAMU_DB_USER": "forge",
            "NAMU_DB_PASSWORD": "secret",
        }
    )

    assert db_set["type"] == "postgresql"
    assert db_set["name"] == "wiki"
    assert db_set["postgresql_host"] == "db"
    assert db_set["postgresql_port"] == "15432"
    assert db_set["postgresql_user"] == "forge"
    assert db_set["postgresql_pw"] == "secret"


def test_env_database_settings는_sqlite를_default로_사용한다():
    db_set = build_database_settings_from_env({})

    assert db_set["type"] == "sqlite"
    assert db_set["name"] == "data"
