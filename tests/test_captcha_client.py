import asyncio

from opennamu_forge.application.dto.captcha import CaptchaVerificationRequest
from opennamu_forge.infrastructure.captcha_client import AiohttpCaptchaClient


class FakeResponse:
    def __init__(self, status, payload):
        self.status = status
        self.payload = payload

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, traceback):
        return False

    async def json(self):
        return self.payload


class FakeSession:
    def __init__(self, response):
        self.response = response
        self.calls = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, traceback):
        return False

    def post(self, url, data):
        self.calls.append((url, data))
        return self.response


def test_captcha_client는_success_true면_true를_반환한다():
    session = FakeSession(FakeResponse(200, {"success": True}))
    client = AiohttpCaptchaClient(lambda: session)

    result = asyncio.run(
        client.verify(
            CaptchaVerificationRequest(
                verify_url="https://captcha.example.com",
                secret="secret",
                response="token",
            )
        )
    )

    assert result is True
    assert session.calls == [
        (
            "https://captcha.example.com",
            {
                "secret": "secret",
                "response": "token",
            },
        )
    ]


def test_captcha_client는_success_false면_false를_반환한다():
    session = FakeSession(FakeResponse(200, {"success": False}))
    client = AiohttpCaptchaClient(lambda: session)

    result = asyncio.run(
        client.verify(
            CaptchaVerificationRequest(
                verify_url="https://captcha.example.com",
                secret="secret",
                response="token",
            )
        )
    )

    assert result is False


def test_captcha_client는_200이_아니면_기존처럼_true를_반환한다():
    session = FakeSession(FakeResponse(500, {"success": False}))
    client = AiohttpCaptchaClient(lambda: session)

    result = asyncio.run(
        client.verify(
            CaptchaVerificationRequest(
                verify_url="https://captcha.example.com",
                secret="secret",
                response="token",
            )
        )
    )

    assert result is True
