from opennamu_forge.application.dto.discussion import TopicCommentDTO
from opennamu_forge.infrastructure.db_model import Topic
from opennamu_forge.infrastructure.mappers.topic_mapper import optional_topic_to_dto, topic_to_dto


def test_topic_mapper는_sqlmodel_row를_dto로_변환한다():
    row = Topic(code="1", id="2", data="body", date="today", ip="tester", block="", top="O")

    assert topic_to_dto(row) == TopicCommentDTO(
        code="1",
        comment_id="2",
        data="body",
        date="today",
        author="tester",
        block="",
        top="O",
    )


def test_topic_mapper는_none을_none으로_변환한다():
    assert optional_topic_to_dto(None) is None
