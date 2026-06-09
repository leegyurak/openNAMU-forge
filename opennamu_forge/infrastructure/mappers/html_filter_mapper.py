from __future__ import annotations

from collections.abc import Sequence

from opennamu_forge.application.dto.html_filter import HtmlFilterDTO
from opennamu_forge.infrastructure.db_model import HtmlFilter


def html_filter_to_dto(row: HtmlFilter) -> HtmlFilterDTO:
    return HtmlFilterDTO(html=row.html, kind=row.kind, plus=row.plus, plus_t=row.plus_t)


def optional_html_filter_to_dto(row: HtmlFilter | None) -> HtmlFilterDTO | None:
    return html_filter_to_dto(row) if row else None


def html_filters_to_dtos(rows: Sequence[HtmlFilter]) -> list[HtmlFilterDTO]:
    return [html_filter_to_dto(row) for row in rows]
