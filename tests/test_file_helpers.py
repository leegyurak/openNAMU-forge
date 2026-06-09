from opennamu_forge.presentation import file_helpers


class FakeSettings:
    def __init__(self, values):
        self.values = values

    def get(self, key, default=""):
        return self.values.get(key, default)


def test_load_image_url은_설정값을_반환한다(monkeypatch):
    monkeypatch.setattr(file_helpers, "get_other_setting_repository", lambda: FakeSettings({"image_where": "uploads"}))

    assert file_helpers.load_image_url() == "uploads"


def test_load_image_url은_기본_이미지_경로를_반환한다(monkeypatch):
    monkeypatch.setattr(file_helpers, "get_other_setting_repository", lambda: FakeSettings({}))

    assert file_helpers.load_image_url() == "data/images"


def test_get_default_robots_txt는_sitemap이_없으면_기본_규칙만_반환한다(monkeypatch):
    monkeypatch.setattr(file_helpers.os.path, "exists", lambda path: False)

    robots = file_helpers.get_default_robots_txt()

    assert "User-agent: *" in robots
    assert "Allow: /w/" in robots
    assert "Sitemap:" not in robots


def test_get_default_robots_txt는_sitemap이_있으면_domain을_포함한다(monkeypatch):
    monkeypatch.setattr(file_helpers.os.path, "exists", lambda path: True)
    monkeypatch.setattr(file_helpers, "load_domain", lambda mode: "https://wiki.example")

    robots = file_helpers.get_default_robots_txt()

    assert "Sitemap: https://wiki.example/sitemap.xml" in robots
