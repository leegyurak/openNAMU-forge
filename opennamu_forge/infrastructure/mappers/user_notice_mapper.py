from __future__ import annotations

from collections.abc import Sequence

from opennamu_forge.application.dto.user_notice import UserNoticeDTO
from opennamu_forge.infrastructure.db_model import UserNotice


def user_notice_to_dto(row: UserNotice) -> UserNoticeDTO:
    return UserNoticeDTO(
        notice_id=row.id,
        user_id=row.name,
        data=row.data,
        date=row.date,
        read=row.readme,
    )


def user_notices_to_dtos(rows: Sequence[UserNotice]) -> list[UserNoticeDTO]:
    return [user_notice_to_dto(row) for row in rows]
