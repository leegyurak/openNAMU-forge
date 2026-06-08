from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from sqlalchemy import Integer, func, update
from sqlalchemy import cast as sa_cast
from sqlmodel import col, select

from opennamu_forge.infrastructure.db_model import History, RecentChange, get_sqlmodel_session


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

    def exists_title(self, title: str) -> bool:
        with get_sqlmodel_session(self.db_set) as session:
            return cast(bool, session.exec(select(func.count()).select_from(History).where(History.title == title)).one() > 0)

    def latest_revision_id(self, title: str) -> str | None:
        with get_sqlmodel_session(self.db_set) as session:
            return session.exec(
                select(History.id).where(History.title == title).order_by(sa_cast(col(History.id), Integer).desc()).limit(1)
            ).first()

    def list_revision_ids_ascending(self, title: str) -> list[str]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(History.id).where(History.title == title).order_by(sa_cast(col(History.id), Integer).asc())).all()

            return cast(list[str], rows)

    def rename_title(self, old_title: str, new_title: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(update(History).where(col(History.title) == old_title).values(title=new_title))
            session.commit()

    def rename_revision_title_and_id(self, old_title: str, old_revision_id: str, new_title: str, new_revision_id: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(
                update(History)
                .where(
                    col(History.title) == old_title,
                    col(History.id) == old_revision_id,
                )
                .values(title=new_title, id=new_revision_id)
            )
            session.commit()

    def rename_recent_change_title(self, old_title: str, new_title: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(update(RecentChange).where(col(RecentChange.title) == old_title).values(title=new_title))
            session.commit()

    def rename_recent_change_title_and_id(self, old_title: str, old_revision_id: str, new_title: str, new_revision_id: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(
                update(RecentChange)
                .where(
                    col(RecentChange.title) == old_title,
                    col(RecentChange.id) == old_revision_id,
                )
                .values(title=new_title, id=new_revision_id)
            )
            session.commit()

    def count_by_ip(self, ip: str) -> int:
        with get_sqlmodel_session(self.db_set) as session:
            return int(session.exec(select(func.count()).select_from(History).where(History.ip == ip)).one())
