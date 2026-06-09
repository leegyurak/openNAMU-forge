from __future__ import annotations

from collections.abc import Sequence

from opennamu_forge.application.dto.discussion import RecentDiscussDTO, TopicCommentDTO
from opennamu_forge.infrastructure.db_model import RecentDiscuss, Topic


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


def topics_to_dtos(rows: Sequence[Topic]) -> list[TopicCommentDTO]:
    return [topic_to_dto(row) for row in rows]


def recent_discuss_to_dto(row: RecentDiscuss) -> RecentDiscussDTO:
    return RecentDiscussDTO(
        title=row.title,
        subtitle=row.sub,
        code=row.code,
        stop=row.stop,
        agree=row.agree,
        acl=row.acl,
    )


def optional_recent_discuss_to_dto(row: RecentDiscuss | None) -> RecentDiscussDTO | None:
    if row is None:
        return None

    return recent_discuss_to_dto(row)
