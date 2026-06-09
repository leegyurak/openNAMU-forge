import os

import pytest

pytestmark = pytest.mark.skipif(
    os.getenv("OPENNAMU_FORGE_POSTGRES_IT") != "1",
    reason="PostgreSQL integration test is enabled only in CI or explicit local runs.",
)


def test_postgresql은_실제_db에_sqlmodel_schema를_생성한다():
    pytest.importorskip("sqlmodel")
    pytest.importorskip("sqlalchemy")

    from opennamu_forge.infrastructure.database_engine import reset_sqlmodel_engine
    from opennamu_forge.infrastructure.migrations import run_schema_migrations

    reset_sqlmodel_engine()
    db_set = {
        "type": "postgresql",
        "name": os.getenv("NAMU_DB", "data"),
        "postgresql_user": os.getenv("NAMU_DB_USER", "opennamu_forge"),
        "postgresql_pw": os.getenv("NAMU_DB_PASSWORD", "opennamu_forge_password"),
        "postgresql_host": os.getenv("NAMU_DB_HOST", "127.0.0.1"),
        "postgresql_port": os.getenv("NAMU_DB_PORT", "5432"),
    }

    result = run_schema_migrations(db_set)

    assert {"data", "history", "other"}.issubset(result.table_names)
    result.engine.dispose()
    reset_sqlmodel_engine()
