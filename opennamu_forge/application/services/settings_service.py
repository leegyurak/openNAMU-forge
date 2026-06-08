from __future__ import annotations

from dataclasses import dataclass

from opennamu_forge.application.dto.settings import SettingKey
from opennamu_forge.application.ports.repositories import OtherSettingPort


@dataclass(frozen=True)
class WikiSettingsService:
    settings: OtherSettingPort

    def get(self, key: SettingKey, *, default: str = "", coverage: str = "") -> str:
        return self.settings.get(key.value, default=default, coverage=coverage)

    def get_dynamic(self, name: str, *, default: str = "", coverage: str = "") -> str:
        return self.settings.get(name, default=default, coverage=coverage)

    def enabled(self, key: SettingKey, *, expected: str = "on") -> bool:
        return self.get(key) == expected
