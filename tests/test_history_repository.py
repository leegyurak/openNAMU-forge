from pathlib import Path

import pytest


@pytest.fixture()
def history_db_set(tmp_path):
    from opennamu_forge.infrastructure.database_config import reset_sqlmodel_engine
    from opennamu_forge.infrastructure.db_model import History, get_sqlmodel_session
    from opennamu_forge.infrastructure.migrations import run_schema_migrations

    db_set = {"type": "sqlite", "name": str(Path(tmp_path) / "history")}
    reset_sqlmodel_engine()
    migration_result = run_schema_migrations(db_set)

    with get_sqlmodel_session(db_set) as session:
        session.add(History(title="FrontPage", id="1", data="body", send=""))
        session.commit()

    yield db_set

    migration_result.engine.dispose()
    reset_sqlmodel_engine()


def test_history_repository는_빈_send도_조회한다(history_db_set):
    from opennamu_forge.infrastructure.history_repository import HistoryRepository

    repository = HistoryRepository(history_db_set)

    assert repository.find_send("FrontPage", "1") == ""


def test_history_repository는_없는_send를_none으로_반환한다(history_db_set):
    from opennamu_forge.infrastructure.history_repository import HistoryRepository

    repository = HistoryRepository(history_db_set)

    assert repository.find_send("Missing", "1") is None


def test_history_repository는_send를_수정한다(history_db_set):
    from opennamu_forge.infrastructure.history_repository import HistoryRepository

    repository = HistoryRepository(history_db_set)

    assert repository.update_send("FrontPage", "1", "memo") is True
    assert repository.find_send("FrontPage", "1") == "memo"


def test_history_repository는_없는_revision_수정을_false로_반환한다(history_db_set):
    from opennamu_forge.infrastructure.history_repository import HistoryRepository

    repository = HistoryRepository(history_db_set)

    assert repository.update_send("Missing", "1", "memo") is False
