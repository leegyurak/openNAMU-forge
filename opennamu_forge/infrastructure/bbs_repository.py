from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from sqlalchemy import Integer, delete, func, or_, update
from sqlalchemy import cast as sa_cast
from sqlmodel import col, select

from opennamu_forge.infrastructure.db_model import BbsData, BbsSet, get_sqlmodel_session


@dataclass(frozen=True)
class BbsRepository:
    db_set: dict[str, str]

    def latest_board_id(self) -> int | None:
        with get_sqlmodel_session(self.db_set) as session:
            return session.exec(select(func.max(sa_cast(col(BbsSet.set_id), Integer))).where(BbsSet.set_name == "bbs_name")).first()

    def get_setting(self, set_id: str, set_name: str, *, set_code: str = "", default: str = "") -> str:
        with get_sqlmodel_session(self.db_set) as session:
            value = select(BbsSet.set_data).where(
                BbsSet.set_id == set_id,
                BbsSet.set_name == set_name,
                BbsSet.set_code == set_code,
            )

            return cast(str, session.exec(select(func.coalesce(value.scalar_subquery(), default))).one())

    def get_data(self, set_id: str, set_name: str, set_code: str, *, default: str = "") -> str:
        with get_sqlmodel_session(self.db_set) as session:
            value = select(BbsData.set_data).where(
                BbsData.set_id == set_id,
                BbsData.set_name == set_name,
                BbsData.set_code == set_code,
            )

            return cast(str, session.exec(select(func.coalesce(value.scalar_subquery(), default))).one())

    def list_board_names(self) -> list[tuple[str, str]]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(col(BbsSet.set_id), col(BbsSet.set_data)).where(BbsSet.set_name == "bbs_name")).all()

            return cast(list[tuple[str, str]], rows)

    def latest_board_post_date(self, set_id: str) -> str:
        with get_sqlmodel_session(self.db_set) as session:
            value = (
                select(BbsData.set_data)
                .where(BbsData.set_id == set_id, BbsData.set_name == "date")
                .order_by(sa_cast(col(BbsData.set_code), Integer).desc())
                .limit(1)
            )

            return cast(str, session.exec(select(func.coalesce(value.scalar_subquery(), ""))).one())

    def list_pinned_post_refs(self, set_id: str) -> list[tuple[str, str, str]]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(
                select(col(BbsData.set_code), col(BbsData.set_id), col(BbsData.set_name))
                .where(BbsData.set_name == "pinned", BbsData.set_id == set_id)
                .order_by(col(BbsData.set_data).desc())
            ).all()

            return cast(list[tuple[str, str, str]], rows)

    def list_title_post_refs(self, set_id: str) -> list[tuple[str, str]]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(
                select(col(BbsData.set_code), col(BbsData.set_id))
                .where(BbsData.set_name == "title", BbsData.set_id == set_id)
                .order_by(sa_cast(col(BbsData.set_code), Integer).desc())
            ).all()

            return cast(list[tuple[str, str]], rows)

    def list_post_refs_by_user(self, user_id: str, *, limit: int = 50) -> list[tuple[str, str]]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(
                select(col(BbsData.set_code), col(BbsData.set_id))
                .where(BbsData.set_name == "user_id", BbsData.set_data == user_id)
                .order_by(col(BbsData.set_data).desc())
                .limit(limit)
            ).all()

            return cast(list[tuple[str, str]], rows)

    def list_comment_refs_by_user(self, user_id: str, *, limit: int = 50) -> list[tuple[str, str]]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(
                select(col(BbsData.set_code), col(BbsData.set_id))
                .where(BbsData.set_name == "comment_user_id", BbsData.set_data == user_id)
                .order_by(col(BbsData.set_data).desc())
                .limit(limit)
            ).all()

            return cast(list[tuple[str, str]], rows)

    def list_recent_post_refs(self, *, limit: int = 50) -> list[tuple[str, str, str]]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(
                select(col(BbsData.set_code), col(BbsData.set_id), col(BbsData.set_data))
                .where(BbsData.set_name == "date")
                .order_by(col(BbsData.set_data).desc())
                .limit(limit)
            ).all()

            return cast(list[tuple[str, str, str]], rows)

    def list_data_rows(self, set_id: str, set_code: str) -> list[tuple[str, str, str, str]]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(
                select(col(BbsData.set_name), col(BbsData.set_data), col(BbsData.set_code), col(BbsData.set_id)).where(
                    BbsData.set_code == set_code,
                    BbsData.set_id == set_id,
                )
            ).all()

            return cast(list[tuple[str, str, str, str]], rows)

    def count_comments_for_post(self, set_id: str) -> int:
        with get_sqlmodel_session(self.db_set) as session:
            return int(
                session.exec(
                    select(func.count()).select_from(BbsData).where(
                        BbsData.set_name == "comment_date",
                        or_(col(BbsData.set_id) == set_id, col(BbsData.set_id).like(set_id + "-%")),
                    )
                ).one()
            )

    def latest_comment_date_for_post(self, set_id: str) -> str:
        with get_sqlmodel_session(self.db_set) as session:
            value = (
                select(BbsData.set_data)
                .where(
                    BbsData.set_name == "comment_date",
                    or_(col(BbsData.set_id) == set_id, col(BbsData.set_id).like(set_id + "-%")),
                )
                .order_by(col(BbsData.set_data).desc())
                .limit(1)
            )

            return cast(str, session.exec(select(func.coalesce(value.scalar_subquery(), "0"))).one())

    def latest_data_code(self, set_id: str, set_name: str) -> int | None:
        with get_sqlmodel_session(self.db_set) as session:
            return session.exec(
                select(func.max(sa_cast(col(BbsData.set_code), Integer))).where(BbsData.set_id == set_id, BbsData.set_name == set_name)
            ).first()

    def add_setting(self, set_id: str, set_name: str, set_data: str, *, set_code: str = "") -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.add(BbsSet(set_id=set_id, set_name=set_name, set_code=set_code, set_data=set_data))
            session.commit()

    def add_data(self, set_id: str, set_name: str, set_code: str, set_data: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.add(BbsData(set_id=set_id, set_name=set_name, set_code=set_code, set_data=set_data))
            session.commit()

    def update_data(self, set_id: str, set_name: str, set_code: str, set_data: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(
                update(BbsData)
                .where(
                    col(BbsData.set_id) == set_id,
                    col(BbsData.set_name) == set_name,
                    col(BbsData.set_code) == set_code,
                )
                .values(set_data=set_data)
            )
            session.commit()

    def delete_board(self, set_id: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(delete(BbsData).where(col(BbsData.set_id) == set_id))
            session.exec(delete(BbsSet).where(col(BbsSet.set_id) == set_id))
            session.exec(delete(BbsData).where(col(BbsData.set_id).like(set_id + "-%")))
            session.commit()

    def delete_post(self, board_id: str, post_id: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(delete(BbsData).where(col(BbsData.set_code) == post_id, col(BbsData.set_id) == board_id))
            session.exec(delete(BbsSet).where(col(BbsSet.set_code) == post_id, col(BbsSet.set_id) == board_id))
            session.exec(delete(BbsData).where(col(BbsData.set_id) == board_id + "-" + post_id))
            session.exec(delete(BbsData).where(col(BbsData.set_id).like(board_id + "-" + post_id + "-%")))
            session.commit()

    def clear_comment(self, set_id: str, set_code: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(update(BbsData).where(col(BbsData.set_code) == set_code, col(BbsData.set_id) == set_id).values(set_data=""))
            session.commit()

    def is_pinned(self, board_id: str, post_id: str) -> bool:
        with get_sqlmodel_session(self.db_set) as session:
            return cast(
                bool,
                session.exec(
                    select(func.count()).select_from(BbsData).where(
                        BbsData.set_code == post_id,
                        BbsData.set_id == board_id,
                        BbsData.set_name == "pinned",
                    )
                ).one()
                > 0,
            )

    def delete_data(self, set_id: str, set_name: str, set_code: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(
                delete(BbsData).where(
                    col(BbsData.set_id) == set_id,
                    col(BbsData.set_name) == set_name,
                    col(BbsData.set_code) == set_code,
                )
            )
            session.commit()
