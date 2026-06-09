from types import SimpleNamespace

import pytest

from opennamu_forge.presentation import user_validation_helpers


class FakeHtmlFilters:
    def __init__(self, filters: tuple[SimpleNamespace, ...] = ()) -> None:
        self.filters = filters

    def list_by_kind(self, kind: str) -> tuple[SimpleNamespace, ...]:
        assert kind == "name"
        return self.filters


class FakeUserSettings:
    def __init__(self, duplicated_user_name: str = "", duplicated_id: str = "") -> None:
        self.duplicated_user_name = duplicated_user_name
        self.duplicated_id = duplicated_id

    def data_exists(self, name: str, data: str) -> bool:
        assert name == "user_name"
        return data == self.duplicated_user_name

    def id_exists(self, user_id: str) -> bool:
        return user_id == self.duplicated_id


def install_user_validation_repositories(
    monkeypatch: pytest.MonkeyPatch,
    html_filters: FakeHtmlFilters,
    user_settings: FakeUserSettings,
) -> None:
    monkeypatch.setattr(user_validation_helpers, "get_html_filter_repository", lambda: html_filters)
    monkeypatch.setattr(user_validation_helpers, "get_user_setting_repository", lambda: user_settings)


@pytest.mark.parametrize(
    ("user_name", "expected"),
    (
        ("valid-user", 0),
        ("<script>", 1),
        ("127.0.0.1", 1),
        ("bad/name", 1),
        ("a" * 129, 1),
    ),
)
def test_사용자명_기본_검증은_기존_반환값을_유지한다(monkeypatch, user_name, expected):
    install_user_validation_repositories(monkeypatch, FakeHtmlFilters(), FakeUserSettings())

    assert user_validation_helpers.do_user_name_check(user_name) == expected


def test_사용자명_필터에_걸리면_거부한다(monkeypatch):
    install_user_validation_repositories(
        monkeypatch,
        FakeHtmlFilters((SimpleNamespace(html="admin"),)),
        FakeUserSettings(),
    )

    assert user_validation_helpers.do_user_name_check("site-admin") == 1


def test_사용자명_표시명_중복이면_거부한다(monkeypatch):
    install_user_validation_repositories(
        monkeypatch,
        FakeHtmlFilters(),
        FakeUserSettings(duplicated_user_name="duplicate"),
    )

    assert user_validation_helpers.do_user_name_check("duplicate") == 1


def test_사용자명_id_중복이면_거부한다(monkeypatch):
    install_user_validation_repositories(
        monkeypatch,
        FakeHtmlFilters(),
        FakeUserSettings(duplicated_id="duplicate"),
    )

    assert user_validation_helpers.do_user_name_check("duplicate") == 1
