from __future__ import annotations

from collections.abc import Sequence

from opennamu_forge.application.dto.history import HistoryRecordDTO
from opennamu_forge.infrastructure.db_model import History


def history_record_to_dto(row: History) -> HistoryRecordDTO:
    return HistoryRecordDTO(
        revision_id=row.id,
        title=row.title,
        date=row.date,
        author=row.ip,
        send=row.send,
        length=row.leng,
        hide=row.hide,
        change_type=row.type,
    )


def history_records_to_dtos(rows: Sequence[History]) -> list[HistoryRecordDTO]:
    return [history_record_to_dto(row) for row in rows]
