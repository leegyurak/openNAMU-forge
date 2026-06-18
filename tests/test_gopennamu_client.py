import asyncio

import pytest

from opennamu_forge.application.dto.gopennamu import GopenNamuRequestContext
from opennamu_forge.infrastructure.gopennamu_client import GopenNamuAiohttpClient, GopenNamuApiError


class FakeResponse:
    def __init__(self, *, text_data="", json_data=None):
        self.text_data = text_data
        self.json_data = {} if json_data is None else json_data

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        return None

    async def text(self):
        return self.text_data

    async def json(self):
        return self.json_data


class FakeSession:
    def __init__(self, response):
        self.response = response
        self.last_method = ""
        self.last_url = ""
        self.last_data = None
        self.last_headers = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        return None

    def get(self, url, *, headers=None):
        self.last_method = "get"
        self.last_url = url
        self.last_headers = headers
        return self.response

    def post(self, url, *, data=None, headers=None):
        self.last_method = "post"
        self.last_url = url
        self.last_data = data
        self.last_headers = headers
        return self.response


def test_gopennamu_client는_same_post를_원래_path로_전달한다():
    session = FakeSession(FakeResponse(text_data="ok"))
    client = GopenNamuAiohttpClient("http://127.0.0.1:3001", session_factory=lambda: session)
    context = GopenNamuRequestContext(
        method="POST",
        path="/w/Test",
        headers={"Cookie": "sid=1"},
        form_data={"name": ["Test"]},
    )

    result = asyncio.run(client.call("same", request_context=context))

    assert result == "ok"
    assert session.last_method == "post"
    assert session.last_url == "http://127.0.0.1:3001/w/Test"
    assert session.last_data == {"name": ["Test"]}
    assert session.last_headers == {"Cookie": "sid=1"}


def test_gopennamu_client는_same_get을_원래_path로_전달한다():
    session = FakeSession(FakeResponse(text_data="page"))
    client = GopenNamuAiohttpClient("http://127.0.0.1:3001/", session_factory=lambda: session)
    context = GopenNamuRequestContext(
        method="GET",
        path="/recent",
        headers={"X-Forwarded-For": "127.0.0.1"},
    )

    result = asyncio.run(client.call("same", request_context=context))

    assert result == "page"
    assert session.last_method == "get"
    assert session.last_url == "http://127.0.0.1:3001/recent"
    assert session.last_headers == {"X-Forwarded-For": "127.0.0.1"}


@pytest.mark.parametrize(
    ("func_name", "expected_method", "expected_result", "expected_data"),
    (
        ("get", "get", "plain", None),
        ("post", "post", "plain", '{"a": "가"}'),
        ("get_json", "get", {"ok": True}, None),
        ("post_json", "post", {"ok": True}, '{"a": "가"}'),
    ),
)
def test_gopennamu_client는_api_path_호출방식을_유지한다(
    func_name,
    expected_method,
    expected_result,
    expected_data,
):
    session = FakeSession(FakeResponse(text_data="plain", json_data={"ok": True}))
    client = GopenNamuAiohttpClient("http://127.0.0.1:3001", session_factory=lambda: session)
    context = GopenNamuRequestContext(headers={"Cookie": "sid=1"})

    result = asyncio.run(client.call(func_name, path="skin_info", other_set={"a": "가"}, request_context=context))

    assert result == expected_result
    assert session.last_method == expected_method
    assert session.last_url == "http://127.0.0.1:3001/api/skin_info"
    assert session.last_data == expected_data
    assert session.last_headers == {"Cookie": "sid=1"}


def test_gopennamu_client는_compatible_api_success를_json으로_반환한다():
    session = FakeSession(FakeResponse(json_data={"response": "ok", "data": {"name": "Wiki"}}))
    client = GopenNamuAiohttpClient("http://127.0.0.1:3001", session_factory=lambda: session)

    result = asyncio.run(client.call("api_func_wiki_set"))

    assert result == {"response": "ok", "data": {"name": "Wiki"}}
    assert session.last_method == "post"
    assert session.last_url == "http://127.0.0.1:3001/compatible_api/api_func_wiki_set"
    assert session.last_data == "{}"


def test_gopennamu_client는_compatible_api_error를_예외로_전환한다():
    session = FakeSession(FakeResponse(json_data={"response": "error"}))
    client = GopenNamuAiohttpClient("http://127.0.0.1:3001", session_factory=lambda: session)

    with pytest.raises(GopenNamuApiError):
        asyncio.run(client.call("api_func_acl", other_set={"name": "FrontPage"}))

    assert session.last_method == "post"
    assert session.last_url == "http://127.0.0.1:3001/compatible_api/api_func_acl"
    assert session.last_data == '{"name": "FrontPage"}'
