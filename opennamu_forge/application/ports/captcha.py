from __future__ import annotations

from typing import Protocol

from opennamu_forge.application.dto.captcha import CaptchaVerificationRequest


class CaptchaClientPort(Protocol):
    async def verify(self, request: CaptchaVerificationRequest) -> bool: ...
