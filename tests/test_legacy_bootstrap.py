from pathlib import Path

import pytest


@pytest.fixture()
def legacy_bootstrap_db_set(tmp_path):
    from opennamu_forge.infrastructure.database_config import reset_sqlmodel_engine
    from opennamu_forge.infrastructure.migrations import run_schema_migrations

    db_set = {"type": "sqlite", "name": str(Path(tmp_path) / "legacy-bootstrap")}
    reset_sqlmodel_engine()
    migration_result = run_schema_migrations(db_set)

    yield db_set

    migration_result.engine.dispose()
    reset_sqlmodel_engine()


def test_legacy_bootstrap_adapter는_legacy_table_column을_보정한다(legacy_bootstrap_db_set):
    from sqlalchemy import inspect

    from opennamu_forge.infrastructure.database_config import get_sqlmodel_engine
    from opennamu_forge.infrastructure.legacy_bootstrap import LegacyBootstrapAdapter

    adapter = LegacyBootstrapAdapter(legacy_bootstrap_db_set)

    adapter.ensure_legacy_schema(None, {"legacy_extra": ["name", "data"]}, "sqlite")

    columns = inspect(get_sqlmodel_engine(legacy_bootstrap_db_set)).get_columns("legacy_extra")

    assert columns[0]["name"] == "test"
    assert columns[1]["name"] == "name"
    assert columns[2]["name"] == "data"
