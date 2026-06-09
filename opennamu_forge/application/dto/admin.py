from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AdminRecordDTO:
    actor: str
    action: str
    time: str
