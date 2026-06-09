from __future__ import annotations

from typing import Protocol

from opennamu_forge.application.dto.email import SmtpEmailConfig


class EmailClientPort(Protocol):
    def send(self, config: SmtpEmailConfig, to_email: str, title: str, body: str) -> bool: ...
