from __future__ import annotations

from opennamu_forge.application.dto.discussion import TopicCommentDTO
from opennamu_forge.infrastructure.db_model import Topic


def topic_to_dto(row: Topic) -> TopicCommentDTO:
    return TopicCommentDTO(
        code=row.code,
        comment_id=row.id,
        data=row.data,
        date=row.date,
        author=row.ip,
        block=row.block,
        top=row.top,
    )


def optional_topic_to_dto(row: Topic | None) -> TopicCommentDTO | None:
    if row is None:
        return None

    return topic_to_dto(row)
