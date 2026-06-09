from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field


@dataclass(frozen=True)
class GopenNamuRequestContext:
    method: str = "GET"
    path: str = ""
    headers: Mapping[str, str] = field(default_factory=dict)
    form_data: Mapping[str, Sequence[str]] | None = None
