from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sqlalchemy import or_


@dataclass(frozen=True)
class UserAgentIdentitySpec:
    first_column: str
    first_value: str
    second_column: str
    second_value: str

    @classmethod
    def two_identities(
        cls,
        first_column: str,
        first_value: str,
        second_column: str,
        second_value: str,
    ) -> UserAgentIdentitySpec:
        return cls(first_column, first_value, second_column, second_value)

    def criteria(self, row_type: Any) -> tuple[Any, ...]:
        first_identity = getattr(row_type, self.first_column)
        second_identity = getattr(row_type, self.second_column)
        return (or_(first_identity == self.first_value, second_identity == self.second_value),)
