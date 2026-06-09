from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import cast

from sqlalchemy import delete, func
from sqlmodel import col, select

from opennamu_forge.application.dto.admin import AdminRecordDTO
from opennamu_forge.infrastructure.db_model import AdminList, AdminRecord, get_sqlmodel_session
from opennamu_forge.infrastructure.mappers.admin_mapper import admin_acls_to_rows, admin_records_to_dtos


@dataclass(frozen=True)
class AdminRepository:
    db_set: dict[str, str]

    def list_group_names(self) -> list[str]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(col(AdminList.name)).distinct().order_by(col(AdminList.name).asc())).all()

            return cast(list[str], rows)

    def list_group_acls(self, name: str) -> list[str]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(col(AdminList.acl)).where(AdminList.name == name).order_by(col(AdminList.acl).asc())).all()

            return cast(list[str], rows)

    def delete_group(self, name: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(delete(AdminList).where(col(AdminList.name) == name))
            session.commit()

    def set_group_acls(self, name: str, acl_names: tuple[str, ...]) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(delete(AdminList).where(col(AdminList.name) == name))
            deque(map(session.merge, admin_acls_to_rows(name, acl_names)), maxlen=0)
            session.commit()

    def list_records(self, *, action_prefix: str = "", offset: int = 0, limit: int = 50) -> list[AdminRecordDTO]:
        action_column = col(AdminRecord.what)
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(
                select(AdminRecord)
                .where(action_column.like(action_prefix + "%"))
                .order_by(col(AdminRecord.time).desc())
                .offset(offset)
                .limit(limit)
            ).all()

            return admin_records_to_dtos(rows)

    def count_records(self, *, action_prefix: str = "") -> int:
        with get_sqlmodel_session(self.db_set) as session:
            return int(session.exec(select(func.count()).select_from(AdminRecord).where(col(AdminRecord.what).like(action_prefix + "%"))).one())

    def latest_record_time(self, *, action_prefix: str = "", default: str = "") -> str:
        with get_sqlmodel_session(self.db_set) as session:
            value = select(AdminRecord.time).where(col(AdminRecord.what).like(action_prefix + "%")).order_by(col(AdminRecord.time).desc()).limit(1)

            return cast(str, session.exec(select(func.coalesce(value.scalar_subquery(), default))).one())

    def delete_records_older_than(self, time: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(delete(AdminRecord).where(col(AdminRecord.time) < time))
            session.commit()
