from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import delete, update
from sqlmodel import col, select

from opennamu_forge.application.dto.user_notice import UserNoticeDTO
from opennamu_forge.infrastructure.db_model import UserNotice, get_sqlmodel_session
from opennamu_forge.infrastructure.mappers.user_notice_mapper import user_notices_to_dtos


@dataclass(frozen=True)
class UserNoticeRepository:
    db_set: dict[str, str]

    def list_by_user(self, user_id: str, *, offset: int = 0, limit: int = 50) -> list[UserNoticeDTO]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(
                select(UserNotice)
                .where(UserNotice.name == user_id)
                .order_by(col(UserNotice.date).desc())
                .offset(offset)
                .limit(limit)
            ).all()

            return user_notices_to_dtos(rows)

    def mark_read(self, user_id: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(update(UserNotice).where(col(UserNotice.name) == user_id).values(readme="1"))
            session.commit()

    def delete(self, user_id: str, notice_id: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(delete(UserNotice).where(col(UserNotice.name) == user_id, col(UserNotice.id) == notice_id))
            session.commit()

    def delete_all(self, user_id: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(delete(UserNotice).where(col(UserNotice.name) == user_id))
            session.commit()
