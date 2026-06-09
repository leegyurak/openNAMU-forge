from __future__ import annotations

from collections.abc import Sequence

from opennamu_forge.application.dto.user_agent import UserAgentDataDTO
from opennamu_forge.infrastructure.db_model import UserAgentData


def user_agent_data_to_dto(row: UserAgentData) -> UserAgentDataDTO:
    return UserAgentDataDTO(name=row.name, ip=row.ip, ua=row.ua, today=row.today)


def user_agent_data_to_dtos(rows: Sequence[UserAgentData]) -> list[UserAgentDataDTO]:
    return [user_agent_data_to_dto(row) for row in rows]
