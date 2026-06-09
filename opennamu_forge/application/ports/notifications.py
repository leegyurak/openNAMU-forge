from __future__ import annotations

from typing import Protocol


class AlarmPort(Protocol):
    async def send_alarm(self, to_user: str, from_user: str, context: str) -> None: ...
