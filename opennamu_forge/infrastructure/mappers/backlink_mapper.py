from __future__ import annotations

from collections.abc import Sequence

from opennamu_forge.infrastructure.db_model import Backlink


def backlink_rows_to_models(rows: Sequence[tuple[str, str, str, str]]) -> list[Backlink]:
    return [Backlink(link=row[0], title=row[1], type=row[2], data=row[3]) for row in rows]
