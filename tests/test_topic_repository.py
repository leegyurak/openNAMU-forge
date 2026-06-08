from pathlib import Path

import pytest


@pytest.fixture()
def topic_db_set(tmp_path):
    from opennamu_forge.infrastructure.database_config import reset_sqlmodel_engine
    from opennamu_forge.infrastructure.db_model import RecentDiscuss, Topic, get_sqlmodel_session
    from opennamu_forge.infrastructure.migrations import run_schema_migrations

    db_set = {"type": "sqlite", "name": str(Path(tmp_path) / "topic")}
    reset_sqlmodel_engine()
    migration_result = run_schema_migrations(db_set)

    with get_sqlmodel_session(db_set) as session:
        session.add(Topic(code="1", id="1", data="comment", top="", block=""))
        session.add(RecentDiscuss(title="FrontPage", sub="topic", code="1", date="2026-01-01 00:00:00"))
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


def test_topic_repository는_recent_discuss_title을_변경한다(topic_db_set):
    from opennamu_forge.infrastructure.topic_repository import TopicRepository

    repository = TopicRepository(topic_db_set)

    assert repository.exists_recent_discuss_title("FrontPage") is True

    repository.rename_recent_discuss_title("FrontPage", "MovedPage")

    assert repository.exists_recent_discuss_title("FrontPage") is False
    assert repository.exists_recent_discuss_title("MovedPage") is True


def test_topic_repository는_ip별_댓글수를_조회한다(topic_db_set):
    from opennamu_forge.infrastructure.topic_repository import TopicRepository

    repository = TopicRepository(topic_db_set)

    assert repository.count_by_ip("") == 1
    assert repository.count_by_ip("missing") == 0
