from __future__ import annotations

from collections.abc import Iterable, Sequence

from opennamu_forge.application.dto.admin import AdminRecordDTO
from opennamu_forge.infrastructure.db_model import AdminList, AdminRecord


def admin_record_to_dto(row: AdminRecord) -> AdminRecordDTO:
    return AdminRecordDTO(actor=row.who, action=row.what, time=row.time)


def admin_records_to_dtos(rows: Sequence[AdminRecord]) -> list[AdminRecordDTO]:
    return [admin_record_to_dto(row) for row in rows]


def admin_acls_to_rows(name: str, acl_names: Iterable[str]) -> list[AdminList]:
    return [AdminList(name=name, acl=acl_name) for acl_name in acl_names]
