from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol

FORGE_BUILD_CHANNEL = "forge"


class VersionSettingReader(Protocol):
    def get(self, name: str, *, coverage: str = "", default: str = "") -> str: ...


def build_version_payload(version_info: Mapping[str, str], settings: VersionSettingReader) -> dict[str, str]:
    _ = settings
    return {
        "version": version_info["r_ver"],
        "db_version": version_info["c_ver"],
        "skin_version": version_info["s_ver"],
        "build": FORGE_BUILD_CHANNEL,
    }
