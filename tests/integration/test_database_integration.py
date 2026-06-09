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
    db_set = {"type": "sqlite", "name": str(Path(tmp_path) / "integration")}

    assert is_sqlmodel_database_type(db_set)

    engine = db_model.init_sqlmodel(db_set)
    table_names = set(inspect(engine).get_table_names())

    assert {"data", "history", "other"}.issubset(table_names)
    engine.dispose()
    reset_sqlmodel_engine()


def test_sqlmodel_session은_세션을_제공한다(tmp_path):
    pytest.importorskip("sqlmodel")

    from opennamu_forge.infrastructure import db_model
    from opennamu_forge.infrastructure.database_engine import reset_sqlmodel_engine

    reset_sqlmodel_engine()
    db_set = {"type": "sqlite", "name": str(Path(tmp_path) / "session")}

    with db_model.get_sqlmodel_session(db_set) as session:
        assert session.bind is not None



def test_sqlmodel은_mysql도_orm_migration을_사용한다():
    from opennamu_forge.config.database import is_sqlmodel_database_type

    assert is_sqlmodel_database_type({"type": "mysql"}) is True
