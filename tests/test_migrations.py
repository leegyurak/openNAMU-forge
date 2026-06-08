from pathlib import Path

import pytest


def test_schema_migration은_sqlmodel_table을_생성한다(tmp_path):
    pytest.importorskip("sqlmodel")

    from opennamu_forge.infrastructure.database_config import reset_sqlmodel_engine
    from opennamu_forge.infrastructure.migrations import run_schema_migrations

    reset_sqlmodel_engine()
    result = run_schema_migrations({"type": "sqlite", "name": str(Path(tmp_path) / "migration")})

    assert {"data", "history", "other"}.issubset(result.table_names)
    result.engine.dispose()
    reset_sqlmodel_engine()


def test_alembic_revision은_sqlmodel_table을_생성한다(tmp_path):
    pytest.importorskip("alembic")
    pytest.importorskip("sqlalchemy")

    from alembic import command
    from sqlalchemy import create_engine, inspect

    from opennamu_forge.infrastructure.migrations import build_alembic_config

    database_path = Path(tmp_path) / "alembic.db"
    database_url = "sqlite:///" + str(database_path)
    command.upgrade(build_alembic_config(database_url), "head")

    engine = create_engine(database_url)
    table_names = set(inspect(engine).get_table_names())

    assert {"alembic_version", "data", "history", "other"}.issubset(table_names)
    engine.dispose()
