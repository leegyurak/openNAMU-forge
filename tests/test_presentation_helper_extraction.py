import asyncio

import flask

from opennamu_forge.presentation import (
    admin_ui_helpers,
    block_helpers,
    edit_toolbar_helpers,
    edit_validation_helpers,
    pagination_helpers,
    password_helpers,
    request_data_helpers,
    skin_helpers,
    user_agent_helpers,
    user_title_helpers,
)
from opennamu_forge.presentation.rendering import render_helpers


class FakeSettings:
    def __init__(self, values=None):
        self.values = {} if values is None else values

    def get(self, name, *, coverage="", default=""):
        return self.values.get(name, default)


class FakeUserSettings:
    def __init__(self):
        self.upserts = []
        self.values = {
            "challenge_first_contribute",
            "challenge_tenth_discussion",
            "challenge_admin",
        }

    def exists(self, user_id, name):
        return name in self.values

    def upsert(self, user_id, name, data):
        self.upserts.append((user_id, name, data))


class FakeRecentBlocks:
    def __init__(self):
        self.closed = []
        self.records = []

    def close_ongoing(self, name, band):
        self.closed.append((name, band))

    def add_record(self, block, end, today, blocker, why, band, ongoing, login):
        self.records.append((block, end, today, blocker, why, band, ongoing, login))


class FakeHtmlFilters:
    def list_by_kind(self, kind):
        return [
            type("Filter", (), {"plus": "A", "html": "Alpha"})(),
        ]

    def list_regex_filters_with_plus(self):
        return [
            type("Filter", (), {"plus": "blocked", "plus_t": "5"})(),
        ]


class FakeHistory:
    def latest_date_by_ip(self, ip):
        return "9999-12-31 23:59:59"


class FakeClassRender:
    def __init__(self, render_lang_data, markup, parameter, render_func):
        self.render_lang_data = render_lang_data

    async def do_render(self, doc_name, doc_data, data_type):
        return ["<p>" + doc_data + "</p>", "console.log('ok')"]


def test_password_helpers는_hash와_legacy_upgrade를_처리한다(monkeypatch):
    users = FakeUserSettings()
    monkeypatch.setattr(password_helpers, "get_other_setting_repository", lambda: FakeSettings({"encode": "sha3", "salt_key": "salt"}))
    monkeypatch.setattr(password_helpers, "get_user_setting_repository", lambda: users)

    encoded = password_helpers.pw_encode("pw", "sha256")
    old_encoded = password_helpers.pw_encode("pw", "sha256")

    assert password_helpers.pw_check("pw", encoded, "sha256", "alice") == 1
    assert password_helpers.pw_encode("pw", "sha3-salt") != old_encoded
    assert users.upserts[0][1] == "pw"
    assert users.upserts[1] == ("alice", "encode", "sha3")


def test_block_helper는_release와_block_record를_기록한다(monkeypatch):
    blocks = FakeRecentBlocks()
    monkeypatch.setattr(block_helpers, "get_recent_block_repository", lambda: blocks)
    monkeypatch.setattr(block_helpers, "get_time", lambda: "2026-06-09 12:00:00")

    block_helpers.ban_insert("alice", "0", "why", "", "admin")
    block_helpers.ban_insert("alice", "0", "why", "", "admin", release=1)

    assert blocks.closed == [("alice", ""), ("alice", "")]
    assert blocks.records[0] == ("alice", "", "2026-06-09 12:00:00", "admin", "why", "", "1", "")
    assert blocks.records[1] == ("alice", "release", "2026-06-09 12:00:00", "admin", "why", "", "", "")


def test_pagination_helper는_previous_next_link를_렌더링한다(monkeypatch):
    async def fake_get_lang(data, safe=0):
        return data

    monkeypatch.setattr(pagination_helpers, "get_lang", fake_get_lang)

    assert asyncio.run(pagination_helpers.get_next_page_bottom("/p/{}", 1, [1], end=1)).count("next") == 1
    assert asyncio.run(pagination_helpers.get_next_page_bottom("/p/{}", 2, [], end=1)).count("previous") == 1
    assert asyncio.run(pagination_helpers.get_next_page_bottom("/p/{}", 2, [1], end=1)).count("</a>") == 2


def test_admin_ui_helper는_acl_list를_golang_gateway에_위임한다(monkeypatch):
    async def fake_python_to_golang(name, payload):
        return {"data": [name, payload["type"]]}

    monkeypatch.setattr(admin_ui_helpers, "python_to_golang", fake_python_to_golang)

    assert admin_ui_helpers.get_default_admin_group() == ["owner", "user", "ip", "ban"]
    assert asyncio.run(admin_ui_helpers.get_acl_list("user")) == ["api_list_acl", "user_document"]


def test_skin_helpers는_skin과_wiki설정을_조회한다(monkeypatch):
    async def fake_get_lang(data, safe=0):
        return data

    async def fake_python_to_golang(name, payload):
        if name == "api_func_skin_name":
            return {"data": "views/ringo/index.html"}
        return {"data": name}

    monkeypatch.setattr(skin_helpers, "get_lang", fake_get_lang)
    monkeypatch.setattr(skin_helpers, "python_to_golang", fake_python_to_golang)
    monkeypatch.setattr(skin_helpers.os, "listdir", lambda path: ["ringo", "main_css"])

    assert asyncio.run(skin_helpers.skin_check()) == "ringo/index.html"
    assert asyncio.run(skin_helpers.wiki_set()) == "api_func_wiki_set"
    assert asyncio.run(skin_helpers.wiki_custom()) == "api_func_wiki_custom"
    assert '<option value="ringo">ringo</option>' in asyncio.run(skin_helpers.load_skin())
    assert asyncio.run(skin_helpers.load_skin("ringo", 1, 1))[0] == "ringo"


def test_request_data_helper는_form과_override_dict를_읽는다():
    form_reader = request_data_helpers.flask_data_or_variable({"a": "form"}, {})
    override_reader = request_data_helpers.flask_data_or_variable({"a": "form"}, {"a": "override"})

    assert form_reader.get("a", "fallback") == "form"
    assert form_reader.get("missing", "fallback") == "fallback"
    assert override_reader.get("a", "fallback") == "override"
    assert override_reader.get("missing", "fallback") == "fallback"


def test_edit_toolbar_helpers는_button과_ip_warning을_렌더링한다(monkeypatch):
    async def fake_get_lang(data, safe=0):
        return data

    monkeypatch.setattr(edit_toolbar_helpers, "get_html_filter_repository", lambda: FakeHtmlFilters())
    monkeypatch.setattr(edit_toolbar_helpers, "get_other_setting_repository", lambda: FakeSettings({"no_login_warning": "warn"}))
    monkeypatch.setattr(edit_toolbar_helpers, "get_lang", fake_get_lang)
    monkeypatch.setattr(edit_toolbar_helpers, "ip_or_user", lambda: 1)

    assert "Alpha" in asyncio.run(edit_toolbar_helpers.edit_button())
    assert "warn" in asyncio.run(edit_toolbar_helpers.ip_warning())


def test_user_agent_helper는_설정이_꺼져있을_때만_기록한다(monkeypatch):
    calls = []
    user_agents = type("UserAgents", (), {"add": lambda self, *args: calls.append(args)})()

    monkeypatch.setattr(user_agent_helpers, "get_other_setting_repository", lambda: FakeSettings({"ua_get": ""}))
    monkeypatch.setattr(user_agent_helpers, "get_user_agent_repository", lambda: user_agents)

    user_agent_helpers.ua_plus("alice", "127.0.0.1", "UA", "today")

    assert calls == [("alice", "127.0.0.1", "UA", "today")]


def test_user_title_helper는_challenge와_admin_title을_반환한다(monkeypatch):
    async def fake_get_lang(data, safe=0):
        return data

    async def fake_acl_check(*args, **kwargs):
        return 0

    monkeypatch.setattr(user_title_helpers, "get_lang", fake_get_lang)
    monkeypatch.setattr(user_title_helpers, "acl_check", fake_acl_check)
    monkeypatch.setattr(user_title_helpers, "get_user_setting_repository", lambda: FakeUserSettings())

    titles = asyncio.run(user_title_helpers.get_user_title_list("alice"))

    assert titles[""] == "default"
    assert titles["🔰"] == "🔰 first_contribute"
    assert titles["💡"] == "💡 tenth_discussion"
    assert titles["☑️"] == "☑️ before_admin"
    assert titles["✅"] == "✅ admin"


def test_edit_validation_helpers는_bottom_text와_title_length를_검증한다(monkeypatch):
    monkeypatch.setattr(
        edit_validation_helpers,
        "get_other_setting_repository",
        lambda: FakeSettings({"edit_bottom_text": "bottom", "title_max_length": "3"}),
    )

    assert edit_validation_helpers.get_edit_text_bottom() == 'bottom<hr class="main_hr">'
    assert edit_validation_helpers.do_title_length_check("FrontPage") == 1


def test_edit_validation_helpers는_checkbox와_send_policy를_검증한다(monkeypatch):
    app = flask.Flask(__name__)
    app.secret_key = "test"

    async def fake_acl_check(*args, **kwargs):
        return 1

    monkeypatch.setattr(
        edit_validation_helpers,
        "get_other_setting_repository",
        lambda: FakeSettings({"copyright_checkbox_text": "agree", "edit_bottom_compulsion": "1"}),
    )
    monkeypatch.setattr(edit_validation_helpers, "acl_check", fake_acl_check)

    with app.test_request_context("/"):
        assert "agree" in edit_validation_helpers.get_edit_text_bottom_check_box()
        assert edit_validation_helpers.do_edit_text_bottom_check_box_check("") == 1
        assert asyncio.run(edit_validation_helpers.do_edit_send_check("")) == 1


def test_edit_validation_helpers는_slow와_filter_policy를_검증한다(monkeypatch):
    async def fake_acl_check(*args, **kwargs):
        return 1

    users = FakeUserSettings()
    bans = []

    monkeypatch.setattr(edit_validation_helpers, "acl_check", fake_acl_check)
    monkeypatch.setattr(edit_validation_helpers, "ip_check", lambda: "alice")
    monkeypatch.setattr(edit_validation_helpers, "get_other_setting_repository", lambda: FakeSettings({"slow_edit": "60"}))
    monkeypatch.setattr(edit_validation_helpers, "get_history_repository", lambda: FakeHistory())
    monkeypatch.setattr(edit_validation_helpers, "get_html_filter_repository", lambda: FakeHtmlFilters())
    monkeypatch.setattr(edit_validation_helpers, "get_user_setting_repository", lambda: users)
    monkeypatch.setattr(edit_validation_helpers, "ban_insert", lambda *args: bans.append(args))

    assert asyncio.run(edit_validation_helpers.do_edit_slow_check()) == 1
    assert asyncio.run(edit_validation_helpers.do_edit_filter("blocked text")) == 1
    assert users.upserts[0] == ("alice", "edit_filter", "blocked text")
    assert bans[0][0] == "alice"


def test_render_helper는_acl_block과_renderer_output을_처리한다(monkeypatch):
    app = flask.Flask(__name__)
    app.secret_key = "test"

    async def allowed_acl(*args, **kwargs):
        return 0

    async def blocked_acl(*args, **kwargs):
        return 1

    async def fake_get_lang(data, safe=0):
        return data

    monkeypatch.setattr(render_helpers, "get_lang", fake_get_lang)
    monkeypatch.setattr(render_helpers, "get_other_setting_repository", lambda: FakeSettings())
    monkeypatch.setattr(render_helpers, "class_do_render", FakeClassRender)
    monkeypatch.setattr(render_helpers, "ip_check", lambda: "alice")
    monkeypatch.setattr(render_helpers, "get_main_skin_set", lambda session, name, ip: "default")

    with app.test_request_context("/"):
        monkeypatch.setattr(render_helpers, "acl_check", blocked_acl)
        assert asyncio.run(render_helpers.render_set("A", "body", "api_view")) == ["", ""]

        monkeypatch.setattr(render_helpers, "acl_check", allowed_acl)
        rendered = asyncio.run(render_helpers.render_set("A", "body"))

    assert '<div class="opennamu_forge_render_complete"><p>body</p></div>' in rendered
    assert "console.log('ok')" in rendered
