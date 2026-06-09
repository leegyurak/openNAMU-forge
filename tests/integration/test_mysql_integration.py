import os

import pytest

pytestmark = pytest.mark.skipif(
    os.getenv("OPENNAMU_FORGE_MYSQL_IT") != "1"
    and not (os.getenv("CI") == "true" and os.getenv("NAMU_DB_TYPE") == "mysql"),
    reason="MySQL integration test requires explicit local opt-in or CI MySQL service config.",
)


def test_mysql은_실제_db에_sqlmodel_schema를_생성한다():
    pytest.importorskip("sqlmodel")
    pytest.importorskip("sqlalchemy")

    from opennamu_forge.infrastructure.database_engine import reset_sqlmodel_engine
    from opennamu_forge.infrastructure.migrations import run_schema_migrations

    reset_sqlmodel_engine()
    database_options = {
        "type": "mysql",
        "name": os.getenv("NAMU_DB", "data"),
        "mysql_user": os.getenv("NAMU_DB_USER", "opennamu_forge"),
        "mysql_pw": os.getenv("NAMU_DB_PASSWORD", "opennamu_forge_password"),
        "mysql_host": os.getenv("NAMU_DB_HOST", "127.0.0.1"),
        "mysql_port": os.getenv("NAMU_DB_PORT", "3306"),
    }

    result = run_schema_migrations(database_options)

    assert {"data", "history", "other"}.issubset(result.table_names)
    result.engine.dispose()
    reset_sqlmodel_engine()


def test_mysql은_migration_후_metrics_route를_제공한다():
    pytest.importorskip("sqlmodel")
    pytest.importorskip("sqlalchemy")

    from opennamu_forge.infrastructure.database_engine import reset_sqlmodel_engine
    from opennamu_forge.infrastructure.migrations import run_schema_migrations
    from opennamu_forge.presentation.flask_factory import create_flask_app

    reset_sqlmodel_engine()
    database_options = {
        "type": "mysql",
        "name": os.getenv("NAMU_DB", "data"),
        "mysql_user": os.getenv("NAMU_DB_USER", "opennamu_forge"),
        "mysql_pw": os.getenv("NAMU_DB_PASSWORD", "opennamu_forge_password"),
        "mysql_host": os.getenv("NAMU_DB_HOST", "127.0.0.1"),
        "mysql_port": os.getenv("NAMU_DB_PORT", "3306"),
    }

    result = run_schema_migrations(database_options)
    app = create_flask_app(base_dir=".", run_mode="", version="test-version", db_type="mysql")

    assert app.test_client().get("/metrics").status_code == 200
    result.engine.dispose()
    reset_sqlmodel_engine()
