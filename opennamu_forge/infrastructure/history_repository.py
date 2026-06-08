from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import update
from sqlmodel import col, select

from opennamu_forge.infrastructure.db_model import History, get_sqlmodel_session


@dataclass(frozen=True)
class HistoryRepository:
    db_set: dict[str, str]

    def find_send(self, title: str, revision_id: str) -> str | None:
        with get_sqlmodel_session(self.db_set) as session:
            return session.exec(
                select(History.send).where(
                    History.title == title,
                    History.id == revision_id,
                )
            ).first()

    def update_send(self, title: str, revision_id: str, send: str) -> bool:
        with get_sqlmodel_session(self.db_set) as session:
            result = session.exec(
                update(History)
                .where(
                    col(History.title) == title,
                    col(History.id) == revision_id,
                )
                .values(send=send)
            )
            session.commit()
            return result.rowcount > 0
