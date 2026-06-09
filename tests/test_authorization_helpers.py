import asyncio

import pytest

from opennamu_forge.presentation import authorization_helpers


def test_level_check는_gopennamu_level_api_결과를_반환한다(monkeypatch):
    calls = []

    async def fake_python_to_golang(func_name, other_set):
        calls.append((func_name, other_set))
        return {"data": {"level": "owner"}}

    monkeypatch.setattr(authorization_helpers, "ip_check", lambda: "127.0.0.1")
    monkeypatch.setattr(authorization_helpers, "python_to_golang", fake_python_to_golang)

    result = asyncio.run(authorization_helpers.level_check())

    assert result == {"level": "owner"}
    assert calls == [("api_func_level", {"ip": "127.0.0.1"})]


def test_acl_check는_허용이면_0을_반환한다(monkeypatch):
    calls = []

    async def fake_python_to_golang(func_name, other_set):
        calls.append((func_name, other_set))
        return {"data": True}

    monkeypatch.setattr(authorization_helpers, "ip_check", lambda: "127.0.0.1")
    monkeypatch.setattr(authorization_helpers, "python_to_golang", fake_python_to_golang)

    result = asyncio.run(authorization_helpers.acl_check("FrontPage", "render", "3"))

    assert result == 0
    assert calls == [
        (
            "api_func_acl",
            {
                "ip": "127.0.0.1",
                "name": "FrontPage",
                "topic_number": "3",
                "tool": "render",
            },
        )
    ]


def test_acl_check는_거부이면_1을_반환한다(monkeypatch):
    async def fake_python_to_golang(func_name, other_set):
        return {"data": False}

    monkeypatch.setattr(authorization_helpers, "python_to_golang", fake_python_to_golang)

    assert asyncio.run(authorization_helpers.acl_check(ip="192.0.2.1")) == 1


def test_acl_check는_허용되고_memo가_있으면_auth_post를_기록한다(monkeypatch):
    calls = []

    async def fake_python_to_golang(func_name, other_set):
        calls.append((func_name, other_set))
        return {"data": True}

    monkeypatch.setattr(authorization_helpers, "python_to_golang", fake_python_to_golang)

    result = asyncio.run(authorization_helpers.acl_check(ip="192.0.2.1", memo="restart"))

    assert result == 0
    assert calls == [
        (
            "api_func_acl",
            {
                "ip": "192.0.2.1",
                "name": "",
                "topic_number": "",
                "tool": "",
            },
        ),
        ("api_func_auth_post", {"ip": "192.0.2.1", "what": "restart"}),
    ]


@pytest.mark.parametrize(
    ("ban_response", "expected"),
    (
        ("true", [1, "login"]),
        ("false", [0, ""]),
    ),
)
def test_ban_check는_ban_문자열을_숫자로_변환한다(monkeypatch, ban_response, expected):
    calls = []

    async def fake_python_to_golang(func_name, other_set):
        calls.append((func_name, other_set))
        return {"ban": ban_response, "ban_type": expected[1]}

    monkeypatch.setattr(authorization_helpers, "ip_check", lambda: "127.0.0.1")
    monkeypatch.setattr(authorization_helpers, "python_to_golang", fake_python_to_golang)

    result = asyncio.run(authorization_helpers.ban_check(tool="login"))

    assert result == expected
    assert calls == [("api_func_ban", {"ip": "127.0.0.1", "type": "login"})]
