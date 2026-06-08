from pathlib import Path

import pytest


@pytest.fixture()
def history_db_set(tmp_path):
    from opennamu_forge.infrastructure.database_config import reset_sqlmodel_engine
    from opennamu_forge.infrastructure.db_model import History, RecentChange, get_sqlmodel_session
    from opennamu_forge.infrastructure.migrations import run_schema_migrations

    db_set = {"type": "sqlite", "name": str(Path(tmp_path) / "history")}
    reset_sqlmodel_engine()
    migration_result = run_schema_migrations(db_set)

    with get_sqlmodel_session(db_set) as session:
        session.add(History(title="FrontPage", id="1", data="body", send=""))
        session.add(History(title="FrontPage", id="2", data="body-2", send=""))
        session.add(RecentChange(title="FrontPage", id="1", date="2026-01-01 00:00:00", type="edit"))
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


def test_history_repository는_title_존재를_확인한다(history_db_set):
    from opennamu_forge.infrastructure.history_repository import HistoryRepository

    repository = HistoryRepository(history_db_set)

    assert repository.exists_title("FrontPage") is True
    assert repository.exists_title("Missing") is False


def test_history_repository는_ip별_기여수를_조회한다(history_db_set):
    from opennamu_forge.infrastructure.history_repository import HistoryRepository

    repository = HistoryRepository(history_db_set)

    assert repository.count_by_ip("") == 2
    assert repository.count_by_ip("missing") == 0


def test_history_repository는_revision_id를_정렬해_조회한다(history_db_set):
    from opennamu_forge.infrastructure.history_repository import HistoryRepository

    repository = HistoryRepository(history_db_set)

    assert repository.latest_revision_id("FrontPage") == "2"
    assert repository.list_revision_ids_ascending("FrontPage") == ["1", "2"]


def test_history_repository는_history_title을_변경한다(history_db_set):
    from opennamu_forge.infrastructure.history_repository import HistoryRepository

    repository = HistoryRepository(history_db_set)

    repository.rename_title("FrontPage", "MovedPage")

    assert repository.exists_title("FrontPage") is False
    assert repository.exists_title("MovedPage") is True


def test_history_repository는_revision_title과_id를_변경한다(history_db_set):
    from opennamu_forge.infrastructure.history_repository import HistoryRepository

    repository = HistoryRepository(history_db_set)

    repository.rename_revision_title_and_id("FrontPage", "1", "MovedPage", "3")

    assert repository.find_send("MovedPage", "3") == ""


def test_history_repository는_recent_change를_변경한다(history_db_set):
    from opennamu_forge.infrastructure.db_model import RecentChange, get_sqlmodel_session
    from opennamu_forge.infrastructure.history_repository import HistoryRepository

    repository = HistoryRepository(history_db_set)

    repository.rename_recent_change_title_and_id("FrontPage", "1", "MovedPage", "3")

    with get_sqlmodel_session(history_db_set) as session:
        recent_change = session.get(RecentChange, ("3", "MovedPage"))

    assert recent_change is not None

    repository.rename_recent_change_title("MovedPage", "FinalPage")

    with get_sqlmodel_session(history_db_set) as session:
        recent_change = session.get(RecentChange, ("3", "FinalPage"))

    assert recent_change is not None
