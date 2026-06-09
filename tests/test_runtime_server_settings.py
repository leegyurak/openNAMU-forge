from opennamu_forge.application.runtime_context import clear_runtime_context, get_runtime_value
from opennamu_forge.presentation.runtime import server_settings


class FakeSettings:
    def __init__(self, values):
        self.values = values
        self.writes = []

    def get(self, key):
        return self.values.get(key, "")

    def upsert(self, key, value):
        self.writes.append((key, value))


def test_server_settings는_저장값을_우선한다(monkeypatch):
    clear_runtime_context()
    monkeypatch.setattr(
        server_settings,
        "get_init_set_list",
        lambda: {"host": {"display": "host", "default": "0.0.0.0", "require": "text"}},
    )
    settings = FakeSettings({"host": "127.0.0.1"})

    resolved = server_settings.resolve_server_settings(settings, env_get=lambda name: "0.0.0.0")

    assert resolved == {"host": "127.0.0.1"}
    assert settings.writes == []
    assert get_runtime_value("setup_host") == "127.0.0.1"


def test_server_settings는_env값을_저장하고_반환한다(monkeypatch):
    clear_runtime_context()
    monkeypatch.setattr(
        server_settings,
        "get_init_set_list",
        lambda: {"port": {"display": "port", "default": "3000", "require": "text"}},
    )
    settings = FakeSettings({})

    resolved = server_settings.resolve_server_settings(settings, env_get=lambda name: "4000")

    assert resolved == {"port": "4000"}
    assert settings.writes == [("port", "4000")]
    assert get_runtime_value("setup_port") == "4000"


def test_server_settings는_빈_입력에서_기본값을_저장한다(monkeypatch):
    clear_runtime_context()
    monkeypatch.setattr(
        server_settings,
        "get_init_set_list",
        lambda: {"markup": {"display": "markup", "default": "namumark", "require": "text"}},
    )
    settings = FakeSettings({})

    resolved = server_settings.resolve_server_settings(
        settings,
        env_get=lambda name: None,
        input_func=lambda prompt: "",
    )

    assert resolved == {"markup": "namumark"}
    assert settings.writes == [("markup", "namumark")]
    assert get_runtime_value("setup_markup") == "namumark"


def test_server_settings는_select_범위_밖_입력을_기본값으로_바꾼다(monkeypatch):
    clear_runtime_context()
    monkeypatch.setattr(
        server_settings,
        "get_init_set_list",
        lambda: {
            "language": {
                "display": "language",
                "default": "ko-KR",
                "require": "select",
                "list": ["ko-KR", "en-US"],
            }
        },
    )
    settings = FakeSettings({})

    resolved = server_settings.resolve_server_settings(
        settings,
        env_get=lambda name: None,
        input_func=lambda prompt: "fr-FR",
    )

    assert resolved == {"language": "ko-KR"}
    assert settings.writes == [("language", "ko-KR")]
    assert get_runtime_value("setup_language") == "ko-KR"
