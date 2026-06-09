from __future__ import annotations

from collections.abc import Callable
from typing import Any

import aiohttp

from opennamu_forge.application.dto.captcha import CaptchaVerificationRequest


class AiohttpCaptchaClient:
    def __init__(self, session_factory: Callable[[], Any] = aiohttp.ClientSession):
        self._session_factory = session_factory

    async def verify(self, request: CaptchaVerificationRequest) -> bool:
        async with self._session_factory() as session:
            async with session.post(
                request.verify_url,
                data={
                    "secret": request.secret,
                    "response": request.response,
                },
            ) as response:
                if response.status != 200:
                    return True

                payload = await response.json()
                return bool(payload.get("success"))
