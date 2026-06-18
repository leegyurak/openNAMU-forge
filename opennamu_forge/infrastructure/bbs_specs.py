from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sqlalchemy import or_


@dataclass(frozen=True)
class BbsPostCommentSpec:
    set_id: str

    @classmethod
    def for_post(cls, set_id: str) -> BbsPostCommentSpec:
        return cls(set_id)

    def set_id_criteria(self, set_id_column: Any) -> Any:
        return or_(set_id_column == self.set_id, set_id_column.like(self.set_id + "-%"))
