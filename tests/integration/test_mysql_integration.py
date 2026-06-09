import os

import pytest

pytestmark = pytest.mark.skipif(
    os.getenv("OPENNAMU_FORGE_MYSQL_IT") != "1",
    reason="MySQL integration test is enabled only in CI or explicit local runs.",
)


def test_mysql은_실제_db에_sqlmodel_schema를_생성한다():
    pytest.importorskip("sqlmodel")
    pytest.importorskip("sqlalchemy")

    from opennamu_forge.infrastructure.database_engine import reset_sqlmodel_engine
    from opennamu_forge.infrastructure.migrations import run_schema_migrations

    reset_sqlmodel_engine()
    db_set = {
        "type": "mysql",
        "name": os.getenv("NAMU_DB", "data"),
        "mysql_user": os.getenv("NAMU_DB_USER", "opennamu_forge"),
        "mysql_pw": os.getenv("NAMU_DB_PASSWORD", "opennamu_forge_password"),
        "mysql_host": os.getenv("NAMU_DB_HOST", "127.0.0.1"),
        "mysql_port": os.getenv("NAMU_DB_PORT", "3306"),
    }

    result = run_schema_migrations(db_set)

    assert {"data", "history", "other"}.issubset(result.table_names)
    result.engine.dispose()
    reset_sqlmodel_engine()
