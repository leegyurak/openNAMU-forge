from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UserNoticeDTO:
    notice_id: str
    user_id: str
    data: str
    date: str
    read: str
