from __future__ import annotations

from collections.abc import Sequence

from opennamu_forge.application.dto.vote import VoteDTO
from opennamu_forge.infrastructure.db_model import Vote


def vote_to_dto(row: Vote) -> VoteDTO:
    return VoteDTO(
        name=row.name,
        vote_id=row.id,
        subject=row.subject,
        data=row.data,
        user=row.user,
        type=row.type,
        acl=row.acl,
    )


def optional_vote_to_dto(row: Vote | None) -> VoteDTO | None:
    if row is None:
        return None

    return vote_to_dto(row)


def votes_to_dtos(rows: Sequence[Vote]) -> list[VoteDTO]:
    return [vote_to_dto(row) for row in rows]
