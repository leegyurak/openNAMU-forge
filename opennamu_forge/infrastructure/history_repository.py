from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from sqlalchemy import Integer, case, delete, func, update
from sqlalchemy import cast as sa_cast
from sqlmodel import col, select

from opennamu_forge.application.dto.history import HistoryRecordDTO
from opennamu_forge.infrastructure.db_model import History, RecentChange, get_sqlmodel_session
from opennamu_forge.infrastructure.mappers.history_mapper import history_records_to_dtos


@dataclass(frozen=True)
class HistoryRepository:
    db_set: dict[str, str]

    def find_data(self, title: str, revision_id: str) -> str | None:
        with get_sqlmodel_session(self.db_set) as session:
            return session.exec(
                select(History.data).where(
                    History.title == title,
                    History.id == revision_id,
                )
            ).first()

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

    def is_hidden(self, title: str, revision_id: str) -> bool:
        with get_sqlmodel_session(self.db_set) as session:
            return cast(
                bool,
                session.exec(
                    select(func.count()).select_from(History).where(
                        History.title == title,
                        History.id == revision_id,
                        History.hide == "O",
                    )
                ).one()
                > 0,
            )

    def any_hidden(self, title: str, revision_ids: tuple[str, ...]) -> bool:
        with get_sqlmodel_session(self.db_set) as session:
            return cast(
                bool,
                session.exec(
                    select(func.count()).select_from(History).where(
                        History.title == title,
                        col(History.id).in_(revision_ids),
                        History.hide == "O",
                    )
                ).one()
                > 0,
            )

    def toggle_hidden(self, title: str, revision_id: str) -> bool:
        with get_sqlmodel_session(self.db_set) as session:
            result = session.exec(
                update(History)
                .where(
                    col(History.title) == title,
                    col(History.id) == revision_id,
                )
                .values(hide=case((col(History.hide) == "O", ""), else_="O"))
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

    def earliest_revision_id(self, title: str) -> str | None:
        with get_sqlmodel_session(self.db_set) as session:
            return session.exec(
                select(History.id).where(History.title == title).order_by(sa_cast(col(History.id), Integer).asc()).limit(1)
            ).first()

    def list_revision_ids_ascending(self, title: str) -> list[str]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(History.id).where(History.title == title).order_by(sa_cast(col(History.id), Integer).asc())).all()

            return cast(list[str], rows)

    def list_records_by_title(self, title: str, *, offset: int = 0, limit: int = 50) -> list[HistoryRecordDTO]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(
                select(History)
                .where(History.title == title)
                .order_by(sa_cast(col(History.id), Integer).desc())
                .offset(offset)
                .limit(limit)
            ).all()

            return history_records_to_dtos(rows)

    def list_records_by_title_type(self, title: str, change_type: str, *, offset: int = 0, limit: int = 50) -> list[HistoryRecordDTO]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(
                select(History)
                .where(History.title == title, History.type == change_type)
                .order_by(sa_cast(col(History.id), Integer).desc())
                .offset(offset)
                .limit(limit)
            ).all()

            return history_records_to_dtos(rows)

    def list_records_by_ip(self, ip: str, *, offset: int = 0, limit: int = 50) -> list[HistoryRecordDTO]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(History).where(History.ip == ip).order_by(col(History.date).desc()).offset(offset).limit(limit)).all()

            return history_records_to_dtos(rows)

    def list_records_by_ip_type(self, ip: str, change_type: str, *, offset: int = 0, limit: int = 50) -> list[HistoryRecordDTO]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(
                select(History).where(History.ip == ip, History.type == change_type).order_by(col(History.date).desc()).offset(offset).limit(limit)
            ).all()

            return history_records_to_dtos(rows)

    def list_records(self, *, offset: int = 0, limit: int = 50) -> list[HistoryRecordDTO]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(History).order_by(col(History.date).desc()).offset(offset).limit(limit)).all()

            return history_records_to_dtos(rows)

    def list_records_by_type(self, change_type: str, *, offset: int = 0, limit: int = 50) -> list[HistoryRecordDTO]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(History).where(History.type == change_type).order_by(col(History.date).desc()).offset(offset).limit(limit)).all()

            return history_records_to_dtos(rows)

    def list_recent_change_records_by_type(self, change_type: str, *, limit: int = 50) -> list[HistoryRecordDTO]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(
                select(History)
                .join(RecentChange, (col(History.title) == col(RecentChange.title)) & (col(History.id) == col(RecentChange.id)))
                .where(RecentChange.type == change_type)
                .order_by(col(RecentChange.date).desc())
                .limit(limit)
            ).all()

            return history_records_to_dtos(rows)

    def count_recent_changes_by_type(self, change_type: str) -> int:
        with get_sqlmodel_session(self.db_set) as session:
            return int(session.exec(select(func.count()).select_from(RecentChange).where(RecentChange.type == change_type)).one())

    def oldest_recent_change_ref_by_type(self, change_type: str) -> tuple[str, str] | None:
        with get_sqlmodel_session(self.db_set) as session:
            return session.exec(
                select(col(RecentChange.id), col(RecentChange.title))
                .where(RecentChange.type == change_type)
                .order_by(col(RecentChange.date).asc())
                .limit(1)
            ).first()

    def delete_recent_change(self, title: str, revision_id: str, change_type: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(
                delete(RecentChange).where(
                    col(RecentChange.title) == title,
                    col(RecentChange.id) == revision_id,
                    col(RecentChange.type) == change_type,
                )
            )
            session.commit()

    def add_recent_change(self, title: str, revision_id: str, date: str, change_type: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.add(RecentChange(title=title, id=revision_id, date=date, type=change_type))
            session.commit()

    def add_history(self, title: str, revision_id: str, data: str, date: str, ip: str, send: str, length: str, change_type: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.add(History(title=title, id=revision_id, data=data, date=date, ip=ip, send=send, leng=length, hide="", type=change_type))
            session.commit()

    def delete_revision(self, title: str, revision_id: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(
                delete(History).where(
                    col(History.title) == title,
                    col(History.id) == revision_id,
                )
            )
            session.commit()

    def delete_title(self, title: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(delete(History).where(col(History.title) == title))
            session.commit()

    def delete_by_ip(self, ip: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(delete(History).where(col(History.ip) == ip))
            session.commit()

    def list_lengths_by_ip_date_prefix(self, ip: str, date_prefix: str) -> list[str]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(col(History.leng)).where(History.ip == ip, col(History.date).like(date_prefix + "%"))).all()

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

    def latest_date_by_ip(self, ip: str) -> str | None:
        with get_sqlmodel_session(self.db_set) as session:
            return session.exec(select(History.date).where(History.ip == ip).order_by(col(History.date).desc()).limit(1)).first()
