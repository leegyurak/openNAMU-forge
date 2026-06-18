from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from sqlalchemy import delete, func
from sqlmodel import col, select

from opennamu_forge.application.dto.user_agent import UserAgentDataDTO
from opennamu_forge.infrastructure.db_model import UserAgentData, get_sqlmodel_session
from opennamu_forge.infrastructure.mappers.user_agent_mapper import user_agent_data_to_dtos
from opennamu_forge.infrastructure.user_agent_specs import UserAgentIdentitySpec

UserAgentColumn = str


@dataclass(frozen=True)
class UserAgentDataRepository:
    db_set: dict[str, str]

    def count_distinct_ips_by_identity(self, identity_column: UserAgentColumn, identity_value: str) -> int:
        with get_sqlmodel_session(self.db_set) as session:
            identity = getattr(UserAgentData, identity_column)

            return int(
                session.exec(
                    select(func.count(func.distinct(UserAgentData.ip))).where(identity == identity_value)
                ).one()
            )

    def count_distinct_ips_by_two_identities(
        self,
        first_column: UserAgentColumn,
        first_value: str,
        second_column: UserAgentColumn,
        second_value: str,
    ) -> int:
        with get_sqlmodel_session(self.db_set) as session:
            identity_spec = UserAgentIdentitySpec.two_identities(
                first_column,
                first_value,
                second_column,
                second_value,
            )

            return int(
                session.exec(
                    select(func.count(func.distinct(UserAgentData.ip))).where(*identity_spec.criteria(UserAgentData))
                ).one()
            )

    def list_by_identity(
        self,
        identity_column: UserAgentColumn,
        identity_value: str,
        *,
        offset: int = 0,
        limit: int = 50,
    ) -> list[UserAgentDataDTO]:
        with get_sqlmodel_session(self.db_set) as session:
            identity = getattr(UserAgentData, identity_column)
            rows = session.exec(
                select(UserAgentData)
                .where(identity == identity_value)
                .order_by(col(UserAgentData.today).desc())
                .offset(offset)
                .limit(limit)
            ).all()

            return user_agent_data_to_dtos(rows)

    def list_by_two_identities(
        self,
        first_column: UserAgentColumn,
        first_value: str,
        second_column: UserAgentColumn,
        second_value: str,
        *,
        offset: int = 0,
        limit: int = 50,
    ) -> list[UserAgentDataDTO]:
        with get_sqlmodel_session(self.db_set) as session:
            identity_spec = UserAgentIdentitySpec.two_identities(
                first_column,
                first_value,
                second_column,
                second_value,
            )
            rows = session.exec(
                select(UserAgentData)
                .where(*identity_spec.criteria(UserAgentData))
                .order_by(col(UserAgentData.today).desc())
                .offset(offset)
                .limit(limit)
            ).all()

            return user_agent_data_to_dtos(rows)

    def list_distinct_values_by_identity(
        self,
        value_column: UserAgentColumn,
        identity_column: UserAgentColumn,
        identity_value: str,
        *,
        offset: int = 0,
        limit: int = 50,
    ) -> list[str]:
        with get_sqlmodel_session(self.db_set) as session:
            value = getattr(UserAgentData, value_column)
            identity = getattr(UserAgentData, identity_column)
            rows = session.exec(
                select(func.distinct(value))
                .where(identity == identity_value)
                .order_by(col(UserAgentData.today).desc())
                .offset(offset)
                .limit(limit)
            ).all()

            return cast(list[str], rows)

    def delete(self, name: str, ip: str, today: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(
                delete(UserAgentData).where(
                    col(UserAgentData.name) == name,
                    col(UserAgentData.ip) == ip,
                    col(UserAgentData.today) == today,
                )
            )
            session.commit()

    def delete_older_than(self, today: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(delete(UserAgentData).where(col(UserAgentData.today) < today))
            session.commit()

    def add(self, name: str, ip: str, ua: str, today: str, *, sub: str = "") -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.add(UserAgentData(name=name, ip=ip, ua=ua, today=today, sub=sub))
            session.commit()
