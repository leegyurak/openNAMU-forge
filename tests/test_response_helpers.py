import asyncio
from unittest.mock import Mock

import pytest

from opennamu_forge.presentation import response_helpers


@pytest.fixture(autouse=True)
def test_language_cache를_초기화한다():
    response_helpers.global_lang_data.clear()
    yield
    response_helpers.global_lang_data.clear()


def test_cached_lang은_html_escape를_유지한다():
    response_helpers.global_lang_data["name"] = "&lt;b&gt;"

    result = response_helpers.load_lang("name")

    assert result == "&lt;b&gt;"


def test_cached_lang은_safe_옵션이면_unescape한다():
    response_helpers.global_lang_data["name"] = "&lt;b&gt;"

    result = response_helpers.load_lang("name", safe=1)

    assert result == "<b>"


@pytest.mark.parametrize(
    ("data_type", "expected"),
    [
        ("normal", "wiki.example"),
        ("full", "https://wiki.example"),
    ],
)
def test_load_domain은_setting과_request_host를_조합한다(monkeypatch, data_type, expected):
    settings = Mock()
    settings.get.side_effect = lambda key: {"http_select": "https", "domain": "wiki.example"}.get(key, "")
    monkeypatch.setattr(response_helpers, "get_other_setting_repository", lambda: settings)

    app = response_helpers.flask.Flask(__name__)
    with app.test_request_context("/", base_url="http://request.example"):
        assert response_helpers.load_domain(data_type) == expected


def test_redirect는_full_domain을_사용한다(monkeypatch):
    settings = Mock()
    settings.get.side_effect = lambda key: {"http_select": "https", "domain": "wiki.example"}.get(key, "")
    monkeypatch.setattr(response_helpers, "get_other_setting_repository", lambda: settings)

    app = response_helpers.flask.Flask(__name__)
    with app.test_request_context("/", base_url="http://request.example"):
        result = response_helpers.redirect("/w/Test")

    assert result.status_code == 302
    assert result.headers["Location"] == "https://wiki.example/w/Test"


def test_load_domain은_request_context가_없으면_setting만_사용한다(monkeypatch):
    settings = Mock()
    settings.get.return_value = ""
    monkeypatch.setattr(response_helpers, "get_other_setting_repository", lambda: settings)

    assert response_helpers.load_domain() == ""


def test_uncached_lang은_gopennamu_language_api로_cache를_채운다(monkeypatch):
    async def fake_python_to_golang(path, other_set):
        return {"response": "ok", "data": {"hello": "Hello"}}

    monkeypatch.setattr(response_helpers, "python_to_golang", fake_python_to_golang)

    result = asyncio.run(response_helpers.get_lang("hello"))

    assert result == "Hello"
    assert response_helpers.global_lang_data["hello"] == "Hello"


def test_uncached_lang은_api에_없으면_marker를_반환한다(monkeypatch):
    async def fake_python_to_golang(path, other_set):
        return {"response": "ok", "data": {"hello": "Hello"}}

    monkeypatch.setattr(response_helpers, "python_to_golang", fake_python_to_golang)

    result = asyncio.run(response_helpers.get_lang("missing"))

    assert result == "missing (M)"


def test_render_template은_gopennamu_template_bridge를_호출한다(monkeypatch):
    async def fake_python_to_golang(method, other_set=None, path=""):
        return {"method": method, "other_set": other_set, "path": path}

    monkeypatch.setattr(response_helpers, "python_to_golang", fake_python_to_golang)
    app = response_helpers.flask.Flask(__name__)

    with app.test_request_context("/wiki"):
        result = asyncio.run(response_helpers.render_template("title", "body", "sub", [["menu", "Menu"]]))

    assert result["method"] == "post"
    assert result["path"] == "template"
    assert result["other_set"]["option"]["path"] == "/wiki"


def test_http_warning은_언어_문구를_hidden_span에_넣는다():
    response_helpers.global_lang_data["http_warning"] = "Use HTTPS"

    result = asyncio.run(response_helpers.http_warning())

    assert "opennamu_forge_http_warning_text_lang" in result
    assert "Use HTTPS" in result


def test_render_simple_set은_toc와_footnote를_생성한다():
    response_helpers.global_lang_data["toc"] = "TOC"

    result = asyncio.run(response_helpers.render_simple_set("<h2>Title</h2><p>A</p><sup>Note</sup>"))

    assert 'class="opennamu_forge_TOC"' in result
    assert 'id="s-1"' in result
    assert 'class="opennamu_forge_footnote"' in result
