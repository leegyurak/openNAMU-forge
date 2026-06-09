from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SkinLatestInfo:
    skin_ver: str
