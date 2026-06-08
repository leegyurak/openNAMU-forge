from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from sqlalchemy import delete, func
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

    def upsert(self, user_id: str, name: str, data: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.merge(UserSet(id=user_id, name=name, data=data))
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
