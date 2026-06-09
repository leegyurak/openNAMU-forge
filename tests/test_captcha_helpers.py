import asyncio

from opennamu_forge.application.dto.captcha import CaptchaVerificationRequest
from opennamu_forge.presentation import captcha_helpers


class FakeSettings:
    def __init__(self, rec_ver):
        self.rec_ver = rec_ver

    def get(self, name, *, coverage="", default=""):
        data = {
            "recaptcha": "site-key",
            "sec_re": "secret",
            "recaptcha_ver": self.rec_ver,
        }
        return data.get(name, default)


class FakeCaptchaClient:
    def __init__(self, verified):
        self.verified = verified
        self.calls = []

    async def verify(self, request):
        self.calls.append(request)
        return self.verified


def test_captcha_get은_v2_markup을_반환한다(monkeypatch):
    async def fake_acl_check(name="", tool="", topic_num="", ip="", memo=""):
        return 1

    monkeypatch.setattr(captcha_helpers, "acl_check", fake_acl_check)
    monkeypatch.setattr(captcha_helpers, "get_other_setting_repository", lambda: FakeSettings(""))

    app = captcha_helpers.flask.Flask(__name__)
    app.secret_key = "test"
    with app.test_request_context("/"):
        markup = asyncio.run(captcha_helpers.captcha_get())

    assert "www.google.com/recaptcha/api.js" in markup
    assert 'data-sitekey="site-key"' in markup


def test_captcha_get은_skip이면_empty_string을_반환한다(monkeypatch):
    async def fake_acl_check(name="", tool="", topic_num="", ip="", memo=""):
        return 0

    monkeypatch.setattr(captcha_helpers, "acl_check", fake_acl_check)

    app = captcha_helpers.flask.Flask(__name__)
    app.secret_key = "test"
    with app.test_request_context("/"):
        captcha_helpers.flask.session["recapcha_pass"] = 1
        markup = asyncio.run(captcha_helpers.captcha_get())

    assert markup == ""


def test_captcha_post는_검증_성공시_0을_반환하고_session을_갱신한다(monkeypatch):
    client = FakeCaptchaClient(True)

    async def fake_acl_check(name="", tool="", topic_num="", ip="", memo=""):
        return 1

    monkeypatch.setattr(captcha_helpers, "acl_check", fake_acl_check)
    monkeypatch.setattr(captcha_helpers, "get_other_setting_repository", lambda: FakeSettings("cf"))
    monkeypatch.setattr(captcha_helpers, "get_captcha_client", lambda: client)

    app = captcha_helpers.flask.Flask(__name__)
    app.secret_key = "test"
    with app.test_request_context("/"):
        result = asyncio.run(captcha_helpers.captcha_post("token"))
        pass_count = captcha_helpers.flask.session["recapcha_pass"]

    assert result == 0
    assert pass_count == 5
    assert client.calls == [
        CaptchaVerificationRequest(
            verify_url="https://challenges.cloudflare.com/turnstile/v0/siteverify",
            secret="secret",
            response="token",
        )
    ]


def test_captcha_post는_검증_실패시_1을_반환한다(monkeypatch):
    client = FakeCaptchaClient(False)

    async def fake_acl_check(name="", tool="", topic_num="", ip="", memo=""):
        return 1

    monkeypatch.setattr(captcha_helpers, "acl_check", fake_acl_check)
    monkeypatch.setattr(captcha_helpers, "get_other_setting_repository", lambda: FakeSettings("h"))
    monkeypatch.setattr(captcha_helpers, "get_captcha_client", lambda: client)

    app = captcha_helpers.flask.Flask(__name__)
    app.secret_key = "test"
    with app.test_request_context("/"):
        result = asyncio.run(captcha_helpers.captcha_post("token"))

    assert result == 1
