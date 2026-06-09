from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from sqlalchemy import delete, func, update
from sqlmodel import col, select

from opennamu_forge.infrastructure.db_model import UserSet, get_sqlmodel_session


@dataclass(frozen=True)
class UserSettingRepository:
    db_set: dict[str, str]

    def get(self, user_id: str, name: str, *, default: str = "") -> str:
        with get_sqlmodel_session(self.db_set) as session:
            value = select(UserSet.data).where(
                UserSet.id == user_id,
                UserSet.name == name,
            )

            return cast(str, session.exec(select(func.coalesce(value.scalar_subquery(), default))).one())

    def list_data_by_name(self, name: str) -> list[str]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(col(UserSet.data)).where(UserSet.name == name)).all()

            return cast(list[str], rows)

    def list_id_data_by_name(self, name: str) -> list[tuple[str, str]]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(col(UserSet.id), col(UserSet.data)).where(UserSet.name == name)).all()

            return cast(list[tuple[str, str]], rows)

    def list_id_data_by_name_excluding_data(self, name: str, excluded_data: str) -> list[tuple[str, str]]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(
                select(col(UserSet.id), col(UserSet.data)).where(
                    UserSet.name == name,
                    UserSet.data != excluded_data,
                )
            ).all()

            return cast(list[tuple[str, str]], rows)

    def list_id_data_by_name_ordered_by_data_desc(self, name: str, *, offset: int = 0, limit: int = 50) -> list[tuple[str, str]]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(
                select(col(UserSet.id), col(UserSet.data))
                .where(UserSet.name == name)
                .order_by(col(UserSet.data).desc())
                .offset(offset)
                .limit(limit)
            ).all()

            return cast(list[tuple[str, str]], rows)

    def exists(self, user_id: str, name: str) -> bool:
        with get_sqlmodel_session(self.db_set) as session:
            return cast(
                bool,
                session.exec(
                    select(func.count()).select_from(UserSet).where(
                        UserSet.id == user_id,
                        UserSet.name == name,
                    )
                ).one()
                > 0,
            )

    def id_exists(self, user_id: str) -> bool:
        with get_sqlmodel_session(self.db_set) as session:
            return cast(
                bool,
                session.exec(select(func.count()).select_from(UserSet).where(UserSet.id == user_id)).one() > 0,
            )

    def has_any(self) -> bool:
        with get_sqlmodel_session(self.db_set) as session:
            return cast(bool, session.exec(select(func.count()).select_from(UserSet)).one() > 0)

    def exists_data(self, user_id: str, name: str, data: str) -> bool:
        with get_sqlmodel_session(self.db_set) as session:
            return cast(
                bool,
                session.exec(
                    select(func.count()).select_from(UserSet).where(
                        UserSet.id == user_id,
                        UserSet.name == name,
                        UserSet.data == data,
                    )
                ).one()
                > 0,
            )

    def data_exists(self, name: str, data: str) -> bool:
        with get_sqlmodel_session(self.db_set) as session:
            return cast(
                bool,
                session.exec(
                    select(func.count()).select_from(UserSet).where(
                        UserSet.name == name,
                        UserSet.data == data,
                    )
                ).one()
                > 0,
            )

    def user_data_exists(self, user_id: str, data: str) -> bool:
        with get_sqlmodel_session(self.db_set) as session:
            return cast(
                bool,
                session.exec(
                    select(func.count()).select_from(UserSet).where(
                        UserSet.id == user_id,
                        UserSet.data == data,
                    )
                ).one()
                > 0,
            )

    def find_id_by_name_data(self, name: str, data: str) -> str | None:
        with get_sqlmodel_session(self.db_set) as session:
            return session.exec(
                select(UserSet.id).where(
                    UserSet.name == name,
                    UserSet.data == data,
                )
            ).first()

    def list_ids_by_name_data(self, name: str, data: str) -> list[str]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(
                select(col(UserSet.id)).where(
                    UserSet.name == name,
                    UserSet.data == data,
                )
            ).all()

            return cast(list[str], rows)

    def count_by_name(self, user_id: str, name: str) -> int:
        with get_sqlmodel_session(self.db_set) as session:
            return int(
                session.exec(
                    select(func.count()).select_from(UserSet).where(
                        UserSet.id == user_id,
                        UserSet.name == name,
                    )
                ).one()
            )

    def upsert(self, user_id: str, name: str, data: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.merge(UserSet(id=user_id, name=name, data=data))
            session.commit()

    def add(self, user_id: str, name: str, data: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.add(UserSet(id=user_id, name=name, data=data))
            session.commit()

    def delete(self, user_id: str, name: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(
                delete(UserSet).where(
                    col(UserSet.id) == user_id,
                    col(UserSet.name) == name,
                )
            )
            session.commit()

    def delete_data(self, user_id: str, name: str, data: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(
                delete(UserSet).where(
                    col(UserSet.id) == user_id,
                    col(UserSet.name) == name,
                    col(UserSet.data) == data,
                )
            )
            session.commit()

    def update_user_title_checkmark(self, user_id: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(
                update(UserSet)
                .where(col(UserSet.id) == user_id, col(UserSet.name) == "user_title", col(UserSet.data) == "✅")
                .values(data="☑️")
            )
            session.commit()
