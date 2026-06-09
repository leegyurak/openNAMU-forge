from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CaptchaVerificationRequest:
    verify_url: str
    secret: str
    response: str
