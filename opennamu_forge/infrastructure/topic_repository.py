from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import case, delete, update
from sqlmodel import col, select

from opennamu_forge.application.dto.discussion import TopicCommentDTO
from opennamu_forge.infrastructure.db_model import Topic, get_sqlmodel_session
from opennamu_forge.infrastructure.mappers.topic_mapper import optional_topic_to_dto


@dataclass(frozen=True)
class TopicRepository:
    db_set: dict[str, str]

    def get(self, code: str, comment_id: str) -> TopicCommentDTO | None:
        with get_sqlmodel_session(self.db_set) as session:
            return optional_topic_to_dto(
                session.exec(
                    select(Topic).where(
                        Topic.code == code,
                        Topic.id == comment_id,
                    )
                )
                .first()
            )

    def toggle_top(self, code: str, comment_id: str) -> bool:
        with get_sqlmodel_session(self.db_set) as session:
            result = session.exec(
                update(Topic)
                .where(
                    col(Topic.code) == code,
                    col(Topic.id) == comment_id,
                )
                .values(top=case((col(Topic.top) == "O", ""), else_="O"))
            )
            session.commit()
            return result.rowcount > 0

    def toggle_block(self, code: str, comment_id: str) -> bool:
        with get_sqlmodel_session(self.db_set) as session:
            result = session.exec(
                update(Topic)
                .where(
                    col(Topic.code) == code,
                    col(Topic.id) == comment_id,
                )
                .values(block=case((col(Topic.block) == "O", ""), else_="O"))
            )
            session.commit()
            return result.rowcount > 0

    def delete(self, code: str, comment_id: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(
                delete(Topic).where(
                    col(Topic.code) == code,
                    col(Topic.id) == comment_id,
                )
            )
            session.commit()
