import pytest

from opennamu_forge.config.database import DatabaseConfig, build_database_config_from_env, is_sqlmodel_database_type


@pytest.mark.parametrize("db_type", ("sqlite", "mysql", "postgresql"))
def test_sqlmodel은_지원_db에서_초기화된다(db_type):
    assert is_sqlmodel_database_type({"type": db_type}) is True


def test_sqlmodel_초기화_판단은_type_key를_요구한다():
    with pytest.raises(KeyError):
        is_sqlmodel_database_type({})


def test_env_database_config는_postgres_alias를_정규화한다():
    db_config = build_database_config_from_env(
        {
            "NAMU_DB_TYPE": "postgres",
            "NAMU_DB": "wiki",
            "NAMU_DB_HOST": "db",
            "NAMU_DB_PORT": "15432",
            "NAMU_DB_USER": "forge",
            "NAMU_DB_PASSWORD": "secret",
        }
    )

    assert isinstance(db_config, DatabaseConfig)
    assert db_config.type == "postgresql"
    assert db_config.name == "wiki"
    assert db_config.postgresql_host == "db"
    assert db_config.postgresql_port == "15432"
    assert db_config.postgresql_user == "forge"
    assert db_config.postgresql_pw == "secret"


def test_env_database_config는_sqlite를_default로_사용한다():
    db_config = build_database_config_from_env({})

    assert db_config.type == "sqlite"
    assert db_config.name == "data"


def test_database_config는_runtime_options로_명시_변환된다():
    db_config = build_database_config_from_env({"NAMU_DB_TYPE": "postgresql", "NAMU_DB": "wiki"})

    assert db_config.to_runtime_options()["type"] == "postgresql"
    assert db_config.to_runtime_options()["name"] == "wiki"


def test_mysql_ddl은_text_column에_server_default를_넣지_않는다():
    pytest.importorskip("sqlalchemy")

    from sqlalchemy.dialects import mysql
    from sqlalchemy.schema import CreateTable

    from opennamu_forge.infrastructure import db_model

    ddl = str(CreateTable(db_model.SQLModel.metadata.tables["data_set"]).compile(dialect=mysql.dialect()))

    assert "set_data TEXT NOT NULL" in ddl
    assert "set_data TEXT NOT NULL DEFAULT" not in ddl
