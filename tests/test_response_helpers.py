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


def test_skin_setting_error는_legacy_skin_link를_렌더링하지_않는다(monkeypatch):
    async def fake_get_lang(key, safe=0):
        return key

    async def fake_render_template(name, data, sub, menu, other=None, option=None):
        return {"name": name, "data": data, "menu": menu}

    monkeypatch.setattr(response_helpers, "get_lang", fake_get_lang)
    monkeypatch.setattr(response_helpers, "render_template", fake_render_template)
    app = response_helpers.flask.Flask(__name__)

    with app.test_request_context("/change/skin_set"):
        result = asyncio.run(response_helpers.re_error(5))

    assert result["name"] == "skin_set"
    assert "error_skin_set" in result["data"]
    assert "error_skin_set_old" not in result["data"]
    assert 'href="/skin_set"' not in result["data"]


@pytest.mark.parametrize(
    ("error_code", "expected_status", "expected_title", "expected_body"),
    (
        (1, 400, "error", "no_login_error"),
        (2, 400, "error", "no_exist_user_error"),
        (3, 400, "error", "authority_error"),
        (4, 400, "error", "no_admin_block_error"),
        (8, 400, "error", "same_id_exist_error"),
        (9, 400, "error", "file_exist_error"),
        (10, 400, "error", "password_error"),
        (11, 400, "error", "topic_long_error"),
        (12, 400, "error", "email_error"),
        (13, 400, "error", "recaptcha_error"),
        (14, 400, "error", "extension_filter_list"),
        (15, 400, "error", "edit_record_error"),
        (16, 400, "error", "same_file_error"),
        (17, 400, "error", "file_capacity_error12"),
        (18, 400, "error", "email_send_error"),
        (19, 400, "error", "move_error"),
        (20, 400, "error", "password_diffrent_error"),
        (21, 400, "error", "edit_filter_error"),
        (22, 400, "error", "file_name_error"),
        (23, 400, "error", "regex_error"),
        (24, 400, "error", "fast_edit_error9"),
        (25, 400, "error", "too_many_dec_error"),
        (26, 400, "error", "application_not_found"),
        (27, 400, "error", "invalid_password_error"),
        (28, 400, "error", "watchlist_overflow_error"),
        (29, 400, "error", "copyright_disagreed"),
        (30, 400, "error", "ie_wrong_callback"),
        (33, 400, "error", "restart_fail_error"),
        (35, 400, "error", "same_email_error"),
        (36, 400, "error", "input_email_error"),
        (37, 400, "error", "error_edit_send_request"),
        (38, 400, "error", "error_title_length_too_long123"),
        (39, 400, "error", "error_title_length_too_long77"),
        (40, 400, "error", "error_password_length_too_short8"),
        (41, 400, "error", "timeout_error6"),
        (42, 400, "error", "fast_edit_error15"),
        (43, 400, "application_submitted", "waiting_for_approval"),
        (44, 400, "error", "error_content_length_too_long5000"),
        (45, 400, "error", "cidr_error"),
        (46, 404, "404", "func_404_error"),
        (47, 400, "error", "still_use_auth_error"),
        (48, 400, "error", "xss_data_include_error"),
        (49, 400, "error", "password_same_as_id_error"),
        (999, 400, "error", "???"),
    ),
)
def test_re_error는_error_code별_문구와_status를_렌더링한다(
    monkeypatch,
    error_code,
    expected_status,
    expected_title,
    expected_body,
):
    settings = Mock()
    settings.get.side_effect = lambda key: {
        "upload": "12",
        "slow_edit": "9",
        "title_max_length": "123",
        "title_topic_max_length": "77",
        "password_min_length": "8",
        "edit_timeout": "6",
        "slow_thread": "15",
        "document_content_max_length": "5000",
    }.get(key, "")

    async def fake_get_lang(key, safe=0):
        return key

    async def fake_render_template(name, data, sub, menu, other=None, option=None):
        return {"name": name, "data": data, "sub": sub, "menu": menu}

    monkeypatch.setattr(response_helpers, "get_other_setting_repository", lambda: settings)
    monkeypatch.setattr(response_helpers, "get_lang", fake_get_lang)
    monkeypatch.setattr(response_helpers, "render_template", fake_render_template)

    result, status = asyncio.run(response_helpers.re_error(error_code))

    assert status == expected_status
    assert result["name"] == expected_title
    assert expected_body in result["data"]


@pytest.mark.parametrize(
    ("is_banned", "expected_body"),
    (
        (0, "authority_error"),
        (1, "opennamu_forge_get_user_info"),
    ),
)
def test_re_error_0은_ban상태에_따라_권한문구나_ip를_렌더링한다(monkeypatch, is_banned, expected_body):
    async def fake_get_lang(key, safe=0):
        return key

    async def fake_render_template(name, data, sub, menu, other=None, option=None):
        return {"name": name, "data": data, "sub": sub, "menu": menu}

    async def fake_ban_check():
        return (is_banned,)

    monkeypatch.setattr(response_helpers, "ban_check", fake_ban_check)
    monkeypatch.setattr(response_helpers, "ip_check", lambda: "127.0.0.1")
    monkeypatch.setattr(response_helpers, "get_lang", fake_get_lang)
    monkeypatch.setattr(response_helpers, "render_template", fake_render_template)

    result, status = asyncio.run(response_helpers.re_error(0))

    assert status == 401
    assert result["name"] == "error"
    assert expected_body in result["data"]
