from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HtmlFilterDTO:
    html: str
    kind: str
    plus: str
    plus_t: str
