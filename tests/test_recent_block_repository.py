from pathlib import Path

import pytest


@pytest.fixture()
def recent_block_db_set(tmp_path):
    from opennamu_forge.infrastructure.database_config import reset_sqlmodel_engine
    from opennamu_forge.infrastructure.db_model import RecentBlock, get_sqlmodel_session
    from opennamu_forge.infrastructure.migrations import run_schema_migrations

    db_set = {"type": "sqlite", "name": str(Path(tmp_path) / "recent-block")}
    reset_sqlmodel_engine()
    migration_result = run_schema_migrations(db_set)

    with get_sqlmodel_session(db_set) as session:
        session.add(
            RecentBlock(
                block="alpha",
                end="2026-01-02 00:00:00",
                today="2026-01-01 00:00:00",
                blocker="admin",
                why="",
                band="",
                login="",
                ongoing="1",
            )
        )
        session.commit()

    yield db_set

    migration_result.engine.dispose()
    reset_sqlmodel_engine()


def test_recent_block_repository는_진행중인_block_종료일을_조회한다(recent_block_db_set):
    from opennamu_forge.infrastructure.recent_block_repository import RecentBlockRepository

    repository = RecentBlockRepository(recent_block_db_set)

    assert repository.get_ongoing_end("alpha") == "2026-01-02 00:00:00"
    assert repository.get_ongoing_end("missing", default="fallback") == "fallback"


def test_recent_block_repository는_진행중인_block을_닫고_record를_추가한다(recent_block_db_set):
    from opennamu_forge.infrastructure.recent_block_repository import RecentBlockRepository

    repository = RecentBlockRepository(recent_block_db_set)

    repository.close_ongoing("alpha", "")
    repository.add_record("alpha", "release", "2026-01-03 00:00:00", "admin", "done", "", "", "")

    assert repository.get_ongoing_end("alpha") == ""
