from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VoteDTO:
    name: str
    vote_id: str
    subject: str
    data: str
    user: str
    type: str
    acl: str
