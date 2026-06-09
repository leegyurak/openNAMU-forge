from __future__ import annotations

from collections import deque
from collections.abc import Mapping
from dataclasses import dataclass
from typing import cast

from sqlalchemy import func
from sqlmodel import col, select

from opennamu_forge.infrastructure.db_model import Other, get_sqlmodel_session
from opennamu_forge.infrastructure.mappers.setting_mapper import other_settings_to_rows


@dataclass(frozen=True)
class OtherSettingRepository:
    db_set: dict[str, str]

    def get(self, name: str, *, coverage: str = "", default: str = "") -> str:
        with get_sqlmodel_session(self.db_set) as session:
            value = select(Other.data).where(
                Other.name == name,
                Other.coverage == coverage,
            )

            return cast(str, session.exec(select(func.coalesce(value.scalar_subquery(), default))).one())

    def list_name_data_by_names(self, names: tuple[str, ...], *, coverage: str = "") -> list[tuple[str, str]]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(
                select(col(Other.name), col(Other.data)).where(
                    col(Other.name).in_(names),
                    Other.coverage == coverage,
                )
            ).all()

            return cast(list[tuple[str, str]], rows)

    def exists(self, name: str, *, coverage: str = "") -> bool:
        with get_sqlmodel_session(self.db_set) as session:
            return cast(
                bool,
                session.exec(
                    select(func.count()).select_from(Other).where(
                        Other.name == name,
                        Other.coverage == coverage,
                    )
                ).one()
                > 0,
            )

    def upsert(self, name: str, data: str, *, coverage: str = "") -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.merge(Other(name=name, data=data, coverage=coverage))
            session.commit()

    def ensure(self, name: str, *, default: str = "", coverage: str = "") -> str:
        data = self.get(name, coverage=coverage, default=default)
        self.upsert(name, data, coverage=coverage)
        return data

    def set_many(self, values: Mapping[str, str], *, coverage: str = "") -> None:
        with get_sqlmodel_session(self.db_set) as session:
            deque(map(session.merge, other_settings_to_rows(values, coverage)), maxlen=0)
            session.commit()
