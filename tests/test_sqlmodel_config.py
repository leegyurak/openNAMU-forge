from typing import Any, cast

import pytest


def load_database_config():
    pytest.importorskip("sqlmodel")
    from opennamu_forge.config import database

    return database


def test_postgresql_database_url을_생성한다():
    database = load_database_config()

    url = database.build_sqlmodel_database_url(
        {
            "type": "postgresql",
            "name": "data",
            "postgresql_user": "open namu",
            "postgresql_pw": "pass/word",
            "postgresql_host": "postgres",
            "postgresql_port": 5432,
        }
    )

    assert url == "postgresql+psycopg://open+namu:pass%2Fword@postgres:5432/data"


def test_postgresql_database_url은_특수문자를_escape한다():
    database = load_database_config()

    url = database.build_sqlmodel_database_url(
        {
            "type": "postgresql",
            "name": "data",
            "postgresql_user": "user@example.com",
            "postgresql_pw": "p@ss:word",
            "postgresql_host": "postgres",
            "postgresql_port": "5432",
        }
    )

    assert url == "postgresql+psycopg://user%40example.com:p%40ss%3Aword@postgres:5432/data"


def test_sqlite_database_url을_생성한다():
    database = load_database_config()

    assert database.build_sqlmodel_database_url({"type": "sqlite", "name": "data"}) == "sqlite:///data.db"


def test_mysql_database_url을_생성한다():
    database = load_database_config()

    url = database.build_sqlmodel_database_url(
        {
            "type": "mysql",
            "name": "data",
            "mysql_user": "open namu",
            "mysql_pw": "pass/word",
            "mysql_host": "mysql",
            "mysql_port": 3306,
        }
    )

    assert url == "mysql+pymysql://open+namu:pass%2Fword@mysql:3306/data?charset=utf8mb4"


def test_mysql_database_url은_문자열_port를_허용한다():
    database = load_database_config()

    url = database.build_sqlmodel_database_url(
        {
            "type": "mysql",
            "name": "data",
            "mysql_user": "root",
            "mysql_pw": "pass",
            "mysql_host": "mysql",
            "mysql_port": "3307",
        }
    )

    assert url == "mysql+pymysql://root:pass@mysql:3307/data?charset=utf8mb4"


def test_sqlite_database_url은_경로형_name을_그대로_사용한다(tmp_path):
    database = load_database_config()

    db_name = str(tmp_path / "wiki")

    assert database.build_sqlmodel_database_url({"type": "sqlite", "name": db_name}) == f"sqlite:///{db_name}.db"


def test_지원하지_않는_database_type은_예외를_낸다():
    database = load_database_config()

    with pytest.raises(ValueError, match="Unsupported database type"):
        database.build_sqlmodel_database_url({"type": "oracle"})


def test_sqlmodel_schema는_기존_other_column을_primary_key로_사용한다():
    pytest.importorskip("sqlmodel")
    from opennamu_forge.infrastructure import db_model

    other_table = cast(Any, db_model.Other).__table__

    assert set(other_table.primary_key.columns.keys()) == {"name", "coverage"}
