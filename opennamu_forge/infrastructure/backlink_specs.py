from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sqlalchemy import or_


@dataclass(frozen=True)
class BacklinkRedirectSpec:
    value: str

    @classmethod
    def title_or_link(cls, value: str) -> BacklinkRedirectSpec:
        return cls(value)

    def criteria(self, title_column: Any, link_column: Any, type_column: Any) -> tuple[Any, ...]:
        return (or_(title_column == self.value, link_column == self.value), type_column == "redirect")
