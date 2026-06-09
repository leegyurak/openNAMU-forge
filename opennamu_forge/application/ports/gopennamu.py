from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol

from opennamu_forge.application.dto.gopennamu import GopenNamuRequestContext


class GopenNamuPort(Protocol):
    async def call(
        self,
        func_name: str,
        *,
        other_set: Mapping[str, Any] | None = None,
        path: str = "",
        request_context: GopenNamuRequestContext | None = None,
    ) -> Any: ...
