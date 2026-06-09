from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AclEntryDTO:
    title: str
    data: str
    acl_type: str
