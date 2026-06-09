from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HistoryRecordDTO:
    revision_id: str
    title: str
    date: str
    author: str
    send: str
    length: str
    hide: str
    change_type: str
