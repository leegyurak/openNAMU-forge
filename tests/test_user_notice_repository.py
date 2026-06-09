from pathlib import Path

import pytest


@pytest.fixture()
def user_notice_db_set(tmp_path):
    from opennamu_forge.infrastructure.database_engine import reset_sqlmodel_engine
    from opennamu_forge.infrastructure.db_model import UserNotice, get_sqlmodel_session
    from opennamu_forge.infrastructure.migrations import run_schema_migrations

    db_set = {"type": "sqlite", "name": str(Path(tmp_path) / "user-notice")}
    reset_sqlmodel_engine()
    migration_result = run_schema_migrations(db_set)

    with get_sqlmodel_session(db_set) as session:
        session.add(UserNotice(id="1", name="tester", data="Alpha", date="2026-01-01 00:00:00", readme=""))
        session.add(UserNotice(id="2", name="tester", data="Beta", date="2026-01-02 00:00:00", readme=""))
        session.add(UserNotice(id="1", name="other", data="Other", date="2026-01-03 00:00:00", readme=""))
        session.commit()

    yield db_set

    migration_result.engine.dispose()
    reset_sqlmodel_engine()


def test_user_notice_repository는_user별_notice를_최신순으로_조회한다(user_notice_db_set):
    from opennamu_forge.infrastructure.user_notice_repository import UserNoticeRepository

    repository = UserNoticeRepository(user_notice_db_set)

    notices = repository.list_by_user("tester")

    assert [notices[0].notice_id, notices[1].notice_id] == ["2", "1"]


def test_user_notice_repository는_notice를_읽음으로_표시한다(user_notice_db_set):
    from opennamu_forge.infrastructure.user_notice_repository import UserNoticeRepository

    repository = UserNoticeRepository(user_notice_db_set)

    repository.mark_read("tester")
    notices = repository.list_by_user("tester")

    assert notices[0].read == "1"
    assert notices[1].read == "1"


def test_user_notice_repository는_notice를_삭제한다(user_notice_db_set):
    from opennamu_forge.infrastructure.user_notice_repository import UserNoticeRepository

    repository = UserNoticeRepository(user_notice_db_set)

    repository.delete("tester", "1")
    notices = repository.list_by_user("tester")

    assert len(notices) == 1
    assert notices[0].notice_id == "2"


def test_user_notice_repository는_user_notice를_전체_삭제한다(user_notice_db_set):
    from opennamu_forge.infrastructure.user_notice_repository import UserNoticeRepository

    repository = UserNoticeRepository(user_notice_db_set)

    repository.delete_all("tester")

    assert repository.list_by_user("tester") == []
    assert repository.list_by_user("other")[0].notice_id == "1"
