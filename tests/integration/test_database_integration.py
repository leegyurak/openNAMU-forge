from pathlib import Path

import pytest


def test_sqlmodel은_sqlite_스키마를_생성한다(tmp_path):
    pytest.importorskip("sqlmodel")
    pytest.importorskip("sqlalchemy")

    from sqlalchemy import inspect

    from opennamu_forge.config.database import is_sqlmodel_database_type
    from opennamu_forge.infrastructure import db_model
    from opennamu_forge.infrastructure.database_engine import reset_sqlmodel_engine

    reset_sqlmodel_engine()
    database_options = {"type": "sqlite", "name": str(Path(tmp_path) / "integration")}

    assert is_sqlmodel_database_type(database_options)

    engine = db_model.init_sqlmodel(database_options)
    table_names = set(inspect(engine).get_table_names())

    assert {"data", "history", "other"}.issubset(table_names)
    engine.dispose()
    reset_sqlmodel_engine()


def test_sqlmodel_session은_세션을_제공한다(tmp_path):
    pytest.importorskip("sqlmodel")

    from opennamu_forge.infrastructure import db_model
    from opennamu_forge.infrastructure.database_engine import reset_sqlmodel_engine

    reset_sqlmodel_engine()
    database_options = {"type": "sqlite", "name": str(Path(tmp_path) / "session")}

    with db_model.get_sqlmodel_session(database_options) as session:
        assert session.bind is not None


def test_sqlmodel은_mysql도_orm_migration을_사용한다():
    from opennamu_forge.config.database import is_sqlmodel_database_type

    assert is_sqlmodel_database_type({"type": "mysql"}) is True


def test_sqlite는_migration_후_metrics_route를_제공한다(tmp_path):
    pytest.importorskip("sqlmodel")
    pytest.importorskip("sqlalchemy")

    from opennamu_forge.infrastructure.database_engine import reset_sqlmodel_engine
    from opennamu_forge.infrastructure.migrations import run_schema_migrations
    from opennamu_forge.presentation.flask_factory import create_flask_app

    reset_sqlmodel_engine()
    database_options = {"type": "sqlite", "name": str(Path(tmp_path) / "sqlite-route")}

    result = run_schema_migrations(database_options)
    app = create_flask_app(base_dir=str(tmp_path), run_mode="", version="test-version", db_type="sqlite")

    assert app.test_client().get("/metrics").status_code == 200
    result.engine.dispose()
    reset_sqlmodel_engine()
