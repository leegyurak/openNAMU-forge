from pathlib import Path

import pytest


@pytest.fixture()
def bbs_db_set(tmp_path):
    from opennamu_forge.infrastructure.database_engine import reset_sqlmodel_engine
    from opennamu_forge.infrastructure.db_model import BbsData, BbsSet, get_sqlmodel_session
    from opennamu_forge.infrastructure.migrations import run_schema_migrations

    db_set = {"type": "sqlite", "name": str(Path(tmp_path) / "bbs")}
    reset_sqlmodel_engine()
    migration_result = run_schema_migrations(db_set)

    with get_sqlmodel_session(db_set) as session:
        session.add(BbsSet(set_id="1", set_name="bbs_name", set_code="", set_data="Board"))
        session.add(BbsSet(set_id="1", set_name="bbs_type", set_code="", set_data="comment"))
        session.add(BbsData(set_id="1", set_name="title", set_code="1", set_data="Post"))
        session.add(BbsData(set_id="1", set_name="date", set_code="1", set_data="2026-01-01 00:00:00"))
        session.add(BbsData(set_id="1", set_name="user_id", set_code="1", set_data="tester"))
        session.add(BbsData(set_id="1-1", set_name="comment", set_code="1", set_data="Comment"))
        session.add(BbsData(set_id="1-1", set_name="comment_date", set_code="1", set_data="2026-01-02 00:00:00"))
        session.add(BbsData(set_id="1-1", set_name="comment_user_id", set_code="1", set_data="tester"))
        session.commit()

    yield db_set

    migration_result.engine.dispose()
    reset_sqlmodel_engine()


def test_bbs_repository는_board_setting을_조회한다(bbs_db_set):
    from opennamu_forge.infrastructure.bbs_repository import BbsRepository

    repository = BbsRepository(bbs_db_set)

    assert repository.latest_board_id() == 1
    assert repository.get_setting("1", "bbs_name") == "Board"
    assert repository.get_setting("missing", "bbs_name") == ""


def test_bbs_repository는_setting과_data를_추가한다(bbs_db_set):
    from opennamu_forge.infrastructure.bbs_repository import BbsRepository

    repository = BbsRepository(bbs_db_set)

    repository.add_setting("2", "bbs_name", "Second")
    repository.add_data("2", "title", "1", "Post")

    assert repository.get_setting("2", "bbs_name") == "Second"
    assert repository.get_data("2", "title", "1") == "Post"


def test_bbs_repository는_최신_data_code를_조회하고_data를_수정한다(bbs_db_set):
    from opennamu_forge.infrastructure.bbs_repository import BbsRepository

    repository = BbsRepository(bbs_db_set)

    repository.add_data("1", "title", "2", "Second")
    repository.update_data("1", "title", "2", "Updated")

    assert repository.latest_data_code("1", "title") == 2
    assert repository.get_data("1", "title", "2") == "Updated"


def test_bbs_repository는_board와_post_목록을_조회한다(bbs_db_set):
    from opennamu_forge.infrastructure.bbs_repository import BbsRepository

    repository = BbsRepository(bbs_db_set)

    assert repository.list_board_names() == [("1", "Board")]
    assert repository.latest_board_post_date("1") == "2026-01-01 00:00:00"
    assert repository.list_title_post_refs("1") == [("1", "1")]
    assert repository.list_post_refs_by_user("tester") == [("1", "1")]
    assert repository.list_comment_refs_by_user("tester") == [("1", "1-1")]
    assert repository.list_recent_post_refs() == [("1", "1", "2026-01-01 00:00:00")]
    assert repository.list_data_rows("1", "1")[0] == ("title", "Post", "1", "1")
    assert repository.count_comments_for_post("1-1") == 1
    assert repository.latest_comment_date_for_post("1-1") == "2026-01-02 00:00:00"


def test_bbs_repository는_pinned를_관리한다(bbs_db_set):
    from opennamu_forge.infrastructure.bbs_repository import BbsRepository

    repository = BbsRepository(bbs_db_set)

    assert repository.is_pinned("1", "1") is False
    repository.add_data("1", "pinned", "1", "2026-01-01")
    assert repository.is_pinned("1", "1") is True
    repository.delete_data("1", "pinned", "1")
    assert repository.is_pinned("1", "1") is False


def test_bbs_repository는_comment를_비운다(bbs_db_set):
    from opennamu_forge.infrastructure.bbs_repository import BbsRepository

    repository = BbsRepository(bbs_db_set)

    repository.clear_comment("1-1", "1")

    assert repository.get_data("1-1", "comment", "1") == ""


def test_bbs_repository는_post와_board를_삭제한다(bbs_db_set):
    from opennamu_forge.infrastructure.bbs_repository import BbsRepository

    repository = BbsRepository(bbs_db_set)

    repository.delete_post("1", "1")

    assert repository.get_data("1", "title", "1") == ""
    assert repository.get_data("1-1", "comment", "1") == ""

    repository.delete_board("1")

    assert repository.get_setting("1", "bbs_name") == ""
