from __future__ import annotations

from typing import Protocol

from opennamu_forge.application.dto.skin import SkinLatestInfo


class SkinInfoClientPort(Protocol):
    def fetch_latest_info(self, info_link: str) -> SkinLatestInfo | None: ...
