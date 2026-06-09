from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SmtpEmailConfig:
    username: str
    password: str
    server: str
    port: int
    security: str
    domain: str
    wiki_name: str
