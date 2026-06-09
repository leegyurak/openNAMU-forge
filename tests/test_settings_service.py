from opennamu_forge.application.dto.settings import SettingKey
from opennamu_forge.application.services.settings_service import WikiSettingsService


class FakeSettings:
    def __init__(self) -> None:
        self.values = {
            ("requires_approval", ""): "on",
            ("head", "ringo"): "body",
        }

    def get(self, name, *, coverage="", default=""):
        return self.values.get((name, coverage), default)

    def list_name_data_by_names(self, names, *, coverage=""):
        raise NotImplementedError

    def exists(self, name, *, coverage=""):
        return (name, coverage) in self.values

    def upsert(self, name, data, *, coverage=""):
        self.values[(name, coverage)] = data

    def ensure(self, name, *, default="", coverage=""):
        data = self.get(name, coverage=coverage, default=default)
        self.upsert(name, data, coverage=coverage)
        return data

    def set_many(self, values, *, coverage=""):
        raise NotImplementedError


def test_wiki_settings_service는_setting_key로_조회한다():
    service = WikiSettingsService(FakeSettings())

    assert service.get(SettingKey.REQUIRES_APPROVAL) == "on"


def test_wiki_settings_service는_coverage를_전달한다():
    service = WikiSettingsService(FakeSettings())

    assert service.get(SettingKey.MARKUP, default="namumark") == "namumark"


def test_wiki_settings_service는_enabled를_판별한다():
    service = WikiSettingsService(FakeSettings())

    assert service.enabled(SettingKey.REQUIRES_APPROVAL) is True


def test_wiki_settings_service는_검증된_동적_설정명을_조회한다():
    service = WikiSettingsService(FakeSettings())

    assert service.get_dynamic("head", coverage="ringo") == "body"
