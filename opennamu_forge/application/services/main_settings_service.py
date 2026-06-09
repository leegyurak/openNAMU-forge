from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Protocol

MAIN_SETTING_DEFAULTS: Mapping[int, tuple[str, str]] = {
    0: ("name", "Wiki"),
    2: ("frontpage", "FrontPage"),
    4: ("upload", "2"),
    5: ("skin", ""),
    7: ("reg", ""),
    8: ("ip_view", ""),
    9: ("back_up", ""),
    10: ("port", "3000"),
    11: ("key", ""),
    15: ("encode", "sha3"),
    16: ("host", "0.0.0.0"),
    19: ("slow_edit", ""),
    20: ("requires_approval", ""),
    21: ("backup_where", ""),
    22: ("domain", ""),
    23: ("ua_get", ""),
    24: ("enable_comment", ""),
    26: ("edit_bottom_compulsion", ""),
    27: ("http_select", "http"),
    28: ("title_max_length", ""),
    29: ("title_topic_max_length", ""),
    30: ("password_min_length", ""),
    31: ("wiki_access_password_need", ""),
    32: ("wiki_access_password", ""),
    33: ("history_recording_off", ""),
    34: ("namumark_compatible", ""),
    35: ("user_name_view", ""),
    36: ("link_case_insensitive", ""),
    37: ("move_with_redirect", ""),
    38: ("slow_thread", ""),
    39: ("edit_timeout", "5"),
    40: ("document_content_max_length", ""),
    41: ("backup_count", ""),
    42: ("ua_expiration_date", ""),
    43: ("auth_history_expiration_date", ""),
    44: ("auth_history_off", ""),
    45: ("user_name_level", ""),
    46: ("load_ip_select", ""),
    47: ("not_use_view_count", ""),
}


class MainSettingStore(Protocol):
    def ensure(self, name: str, *, default: str = "", coverage: str = "") -> str: ...
    def set_many(self, values: Mapping[str, str], *, coverage: str = "") -> None: ...


@dataclass(frozen=True)
class MainSettingsFormService:
    settings: MainSettingStore
    secret_key_provider: Callable[[], str]

    def load_form_values(self) -> dict[int, str]:
        values: dict[int, str] = {}

        for index, setting in MAIN_SETTING_DEFAULTS.items():
            values[index] = self.settings.ensure(setting[0], default=self._default_for(setting[0], setting[1]))

        return values

    def update_from_form(self, form: Mapping[str, str]) -> None:
        update_values: dict[str, str] = {}

        for setting_name, default in MAIN_SETTING_DEFAULTS.values():
            update_values[setting_name] = form.get(setting_name, self._default_for(setting_name, default))

        self.settings.set_many(update_values)

    def _default_for(self, setting_name: str, fallback: str) -> str:
        if setting_name == "key" and fallback == "":
            return self.secret_key_provider()

        return fallback
