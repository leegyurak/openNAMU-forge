from __future__ import annotations

from collections.abc import Sequence

from opennamu_forge.application.dto.document_meta import AclEntryDTO
from opennamu_forge.infrastructure.db_model import Acl


def acl_entry_to_dto(row: Acl) -> AclEntryDTO:
    return AclEntryDTO(title=row.title, data=row.data, acl_type=row.type)


def acl_entries_to_dtos(rows: Sequence[Acl]) -> list[AclEntryDTO]:
    return [acl_entry_to_dto(row) for row in rows]
