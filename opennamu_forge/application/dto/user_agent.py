from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UserAgentDataDTO:
    name: str
    ip: str
    ua: str
    today: str
