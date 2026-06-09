import asyncio

import flask

from opennamu_forge.application.dto.settings import SettingKey
from opennamu_forge.presentation import edit_presenter


class FakeDocumentMeta:
    def get(self, name, key):
        return "<div>top:" + name + ":" + key + "</div>"


class FakeWikiSettings:
    def get(self, key):
        values = {
            SettingKey.EDIT_HELP: "Edit help",
            SettingKey.BBS_HELP: "BBS help",
            SettingKey.BBS_COMMENT_HELP: "Comment help",
            SettingKey.TOPIC_TEXT: "Topic help",
        }
        return values[key]


def test_edit_editor는_editor_html을_렌더링한다(monkeypatch):
    app = flask.Flask(__name__)
    app.secret_key = "test"

    async def fake_get_lang(data, safe=0):
        return data

    async def fake_captcha_get():
        return "CAPTCHA"

    async def fake_ip_warning():
        return "IP_WARN"

    async def fake_edit_button():
        return "EDIT_BUTTON"

    monkeypatch.setattr(edit_presenter, "get_document_meta_repository", lambda: FakeDocumentMeta())
    monkeypatch.setattr(edit_presenter, "get_wiki_settings_service", lambda: FakeWikiSettings())
    monkeypatch.setattr(edit_presenter, "get_lang", fake_get_lang)
    monkeypatch.setattr(edit_presenter, "captcha_get", fake_captcha_get)
    monkeypatch.setattr(edit_presenter, "ip_warning", fake_ip_warning)
    monkeypatch.setattr(edit_presenter, "edit_button", fake_edit_button)
    monkeypatch.setattr(edit_presenter, "get_main_skin_set", lambda session, name, ip: "use")

    with app.test_request_context("/", headers={"Cookie": "main_css_darkmode=1"}):
        html = asyncio.run(
            edit_presenter.edit_editor(
                "alice",
                "content",
                addon="ADDON",
                name="FrontPage",
                markup_selector_html="<select>markup</select>",
            )
        )

    assert "Edit help" in html
    assert "top:FrontPage:document_top" in html
    assert "CAPTCHAIP_WARNADDON" in html
    assert "EDIT_BUTTON" in html
    assert "<select>markup</select>" in html
    assert "vs-dark" in html


def test_edit_timeout는_render_set이_끝나면_성공을_반환한다(monkeypatch):
    async def fake_render_set(doc_name, doc_data):
        return doc_name + doc_data

    monkeypatch.setattr(edit_presenter, "render_set", fake_render_set)

    assert asyncio.run(edit_presenter.edit_timeout("FrontPage", "content")) == 0


def test_edit_timeout는_render_set이_느리면_timeout을_반환한다(monkeypatch):
    async def fake_render_set(doc_name, doc_data):
        await asyncio.sleep(1)
        return doc_name + doc_data

    monkeypatch.setattr(edit_presenter, "render_set", fake_render_set)

    assert asyncio.run(edit_presenter.edit_timeout("FrontPage", "content", timeout=0)) == 1
