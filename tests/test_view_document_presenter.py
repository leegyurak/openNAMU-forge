import asyncio

from opennamu_forge.presentation import view_document_presenter


class FakeBacklinks:
    def list_distinct_links_by_title_type(self, title, link_type):
        return ["category:Sub", "Doc"]

    def get_data(self, title, link, link_type):
        if link == "Doc":
            return "Visible Doc"
        return ""

    def exists(self, title, link, link_type):
        return link == "category:Sub"


class FakeImage:
    size = (640, 480)


def test_build_category_view는_sub와_document_category를_렌더링한다(monkeypatch):
    async def fake_get_lang(data, safe=0):
        return data

    monkeypatch.setattr(view_document_presenter, "get_lang", fake_get_lang)
    monkeypatch.setattr(view_document_presenter, "get_main_skin_set", lambda session, name, ip: "on")

    html = asyncio.run(view_document_presenter.build_category_view("category:Root", FakeBacklinks(), {}, "alice"))

    assert "under_category" in html
    assert "category_title" in html
    assert "category:Sub" in html
    assert "Visible Doc" in html
    assert "opennamu_forge_category_blur" in html


def test_build_file_view는_파일_preview와_delete_menu를_반환한다(monkeypatch, tmp_path):
    async def fake_get_lang(data, safe=0):
        return data

    monkeypatch.setattr(view_document_presenter, "get_lang", fake_get_lang)
    monkeypatch.setattr(view_document_presenter, "load_image_url", lambda: str(tmp_path))
    monkeypatch.setattr(view_document_presenter, "sha224_replace", lambda file_name: "hashed-" + file_name)
    monkeypatch.setattr(view_document_presenter.Image, "open", lambda path: FakeImage())
    (tmp_path / "hashed-Example.png").write_bytes(b"image")

    file_html, menu = asyncio.run(view_document_presenter.build_file_view("file:Example.png", "7"))

    assert "/image/hashed-Example.png.cache_v7" in file_html
    assert "640x480" in file_html
    assert menu == [["delete_file/file%3AExample.png", "file_delete"]]


def test_build_file_view는_파일이_없으면_empty를_반환한다(tmp_path, monkeypatch):
    monkeypatch.setattr(view_document_presenter, "load_image_url", lambda: str(tmp_path))
    monkeypatch.setattr(view_document_presenter, "sha224_replace", lambda file_name: "missing")

    file_html, menu = asyncio.run(view_document_presenter.build_file_view("file:Missing.png", "1"))

    assert file_html == ""
    assert menu == []


def test_redirect_notice는_format_실패시_default_format으로_돌아간다():
    html = view_document_presenter.build_redirect_notice("Source", "Target", "{broken", "BODY")

    assert "/w_from/Source" in html
    assert "<b>Target</b>" in html
    assert "BODY" in html


def test_build_trace_view는_recent_document_link를_역순으로_렌더링한다(monkeypatch):
    async def fake_get_lang(data, safe=0):
        return data

    monkeypatch.setattr(view_document_presenter, "get_lang", fake_get_lang)

    html = asyncio.run(view_document_presenter.build_trace_view(["A", "B"], "BODY"))

    assert html.index("/w/B") < html.index("/w/A")
    assert "trace" in html
    assert "BODY" in html
