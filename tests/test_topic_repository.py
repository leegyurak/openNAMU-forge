from pathlib import Path

import pytest


@pytest.fixture()
def topic_db_set(tmp_path):
    from opennamu_forge.infrastructure.database_engine import reset_sqlmodel_engine
    from opennamu_forge.infrastructure.db_model import RecentDiscuss, Topic, TopicSet, get_sqlmodel_session
    from opennamu_forge.infrastructure.migrations import run_schema_migrations

    db_set = {"type": "sqlite", "name": str(Path(tmp_path) / "topic")}
    reset_sqlmodel_engine()
    migration_result = run_schema_migrations(db_set)

    with get_sqlmodel_session(db_set) as session:
        session.add(Topic(code="1", id="1", data="comment", top="", block=""))
        session.add(RecentDiscuss(title="FrontPage", sub="topic", code="1", date="2026-01-01 00:00:00"))
        session.add(TopicSet(thread_code="1", set_name="thread_view_acl", set_id="", set_data="member"))
        session.commit()

    yield db_set

    migration_result.engine.dispose()
    reset_sqlmodel_engine()


def test_topic_repository는_top을_toggle한다(topic_db_set):
    from opennamu_forge.infrastructure.topic_repository import TopicRepository

    repository = TopicRepository(topic_db_set)

    assert repository.toggle_top("1", "1") is True
    comment = repository.get("1", "1")
    assert comment is not None
    assert comment.top == "O"
    assert repository.toggle_top("1", "1") is True
    comment = repository.get("1", "1")
    assert comment is not None
    assert comment.top == ""


def test_topic_repository는_block을_toggle한다(topic_db_set):
    from opennamu_forge.infrastructure.topic_repository import TopicRepository

    repository = TopicRepository(topic_db_set)

    assert repository.toggle_block("1", "1") is True
    comment = repository.get("1", "1")
    assert comment is not None
    assert comment.block == "O"
    assert repository.toggle_block("1", "1") is True
    comment = repository.get("1", "1")
    assert comment is not None
    assert comment.block == ""


def test_topic_repository는_없는_comment_toggle을_false로_반환한다(topic_db_set):
    from opennamu_forge.infrastructure.topic_repository import TopicRepository

    repository = TopicRepository(topic_db_set)

    assert repository.toggle_top("missing", "1") is False


def test_topic_repository는_comment를_삭제한다(topic_db_set):
    from opennamu_forge.infrastructure.topic_repository import TopicRepository

    repository = TopicRepository(topic_db_set)

    repository.delete("1", "1")

    assert repository.get("1", "1") is None


def test_topic_repository는_thread를_삭제한다(topic_db_set):
    from opennamu_forge.infrastructure.topic_repository import TopicRepository

    repository = TopicRepository(topic_db_set)

    repository.delete_thread("1")

    assert repository.get("1", "1") is None
    assert repository.get_recent_discuss("1") is None


def test_topic_repository는_recent_discuss를_조회하고_수정한다(topic_db_set):
    from opennamu_forge.infrastructure.db_model import RecentDiscuss, get_sqlmodel_session
    from opennamu_forge.infrastructure.topic_repository import TopicRepository

    repository = TopicRepository(topic_db_set)

    recent_discuss = repository.get_recent_discuss("1")
    assert recent_discuss is not None
    assert recent_discuss.title == "FrontPage"
    assert recent_discuss.subtitle == "topic"

    repository.update_recent_discuss_title_subtitle("1", "MovedPage", "moved topic")
    repository.update_recent_discuss_stop("1", "O")
    repository.update_recent_discuss_agree("1", "O")
    assert repository.update_recent_discuss_date("1", "2026-01-02 00:00:00") is True

    recent_discuss = repository.get_recent_discuss("1")
    assert recent_discuss is not None
    assert recent_discuss.title == "MovedPage"
    assert recent_discuss.subtitle == "moved topic"
    assert recent_discuss.stop == "O"
    assert recent_discuss.agree == "O"

    with get_sqlmodel_session(topic_db_set) as session:
        saved_recent_discuss = session.get(RecentDiscuss, ("MovedPage", "moved topic", "1"))

    assert saved_recent_discuss is not None
    assert saved_recent_discuss.date == "2026-01-02 00:00:00"

    assert repository.update_recent_discuss_date("2", "2026-01-03 00:00:00") is False
    repository.add_recent_discuss("2", "NewPage", "new topic", "2026-01-03 00:00:00")
    new_recent_discuss = repository.get_recent_discuss("2")
    assert new_recent_discuss is not None
    assert new_recent_discuss.title == "NewPage"


def test_topic_repository는_thread_setting을_조회한다(topic_db_set):
    from opennamu_forge.infrastructure.topic_repository import TopicRepository

    repository = TopicRepository(topic_db_set)

    assert repository.get_thread_setting("1", "thread_view_acl") == "member"
    assert repository.get_thread_setting("1", "missing", default="normal") == "normal"

    repository.upsert_thread_setting("1", "thread_view_acl", "admin")

    assert repository.get_thread_setting("1", "thread_view_acl") == "admin"


def test_topic_repository는_thread_code와_comment_id를_조회한다(topic_db_set):
    from opennamu_forge.infrastructure.topic_repository import TopicRepository

    repository = TopicRepository(topic_db_set)

    assert repository.latest_topic_code() == 1
    assert repository.latest_comment_id("1") == 1
    assert repository.list_comment_ids_ascending("1") == ["1"]
    assert repository.first_comment_author("1") == ""

    repository.add_comment("1", "2", "reply", "2026-01-02 00:00:00", "tester", "")
    added_comment = repository.get("1", "2")

    assert repository.latest_comment_id("1") == 2
    assert added_comment is not None
    assert added_comment.data == "reply"


def test_topic_repository는_recent_discuss_title을_변경한다(topic_db_set):
    from opennamu_forge.infrastructure.topic_repository import TopicRepository

    repository = TopicRepository(topic_db_set)

    assert repository.exists_recent_discuss_title("FrontPage") is True
    assert repository.exists_open_recent_discuss_title("FrontPage") is True

    repository.update_recent_discuss_acl("1", "admin")
    recent_discuss = repository.get_recent_discuss("1")
    assert recent_discuss is not None
    assert recent_discuss.acl == "admin"

    repository.rename_recent_discuss_title("FrontPage", "MovedPage")

    assert repository.exists_recent_discuss_title("FrontPage") is False
    assert repository.exists_recent_discuss_title("MovedPage") is True


def test_topic_repository는_ip별_댓글수를_조회한다(topic_db_set):
    from opennamu_forge.infrastructure.topic_repository import TopicRepository

    repository = TopicRepository(topic_db_set)

    assert repository.count_by_ip("") == 1
    assert repository.count_by_ip("missing") == 0
    assert repository.latest_date_by_ip("") == ""


def test_topic_repository는_ip별_comment를_조회한다(topic_db_set):
    from opennamu_forge.infrastructure.topic_repository import TopicRepository

    repository = TopicRepository(topic_db_set)

    comments = repository.list_by_ip("")

    assert len(comments) == 1
    assert comments[0].code == "1"
    assert comments[0].comment_id == "1"
