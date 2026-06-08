from __future__ import annotations

from collections.abc import Mapping

from opennamu_forge.infrastructure.db_model import Other


def other_settings_to_rows(values: Mapping[str, str], coverage: str) -> list[Other]:
    return [Other(name=name, data=data, coverage=coverage) for name, data in values.items()]
