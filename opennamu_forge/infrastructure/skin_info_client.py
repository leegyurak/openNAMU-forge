from __future__ import annotations

import json
import urllib.request
from collections.abc import Callable
from typing import Any

from opennamu_forge.application.dto.skin import SkinLatestInfo


class SkinInfoClient:
    def __init__(self, urlopen: Callable[[str], Any] = urllib.request.urlopen):
        self._urlopen = urlopen

    def fetch_latest_info(self, info_link: str) -> SkinLatestInfo | None:
        try:
            response = self._urlopen(info_link)
            if response.getcode() != 200:
                return None

            payload = json.loads(response.read().decode())
        except (AttributeError, OSError, UnicodeDecodeError, json.JSONDecodeError):
            return None

        if not isinstance(payload, dict):
            return None

        skin_ver = payload.get("skin_ver")
        if not isinstance(skin_ver, str):
            return None

        return SkinLatestInfo(skin_ver=skin_ver)
