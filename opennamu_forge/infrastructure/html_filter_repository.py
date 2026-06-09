from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from sqlalchemy import delete, func
from sqlmodel import col, select

from opennamu_forge.application.dto.html_filter import HtmlFilterDTO
from opennamu_forge.infrastructure.db_model import HtmlFilter, get_sqlmodel_session
from opennamu_forge.infrastructure.mappers.html_filter_mapper import html_filters_to_dtos, optional_html_filter_to_dto


@dataclass(frozen=True)
class HtmlFilterRepository:
    db_set: dict[str, str]

    def list_by_kind(self, kind: str) -> list[HtmlFilterDTO]:
        with get_sqlmodel_session(self.db_set) as session:
            return html_filters_to_dtos(session.exec(select(HtmlFilter).where(HtmlFilter.kind == kind)).all())

    def list_regex_filters_with_plus(self) -> list[HtmlFilterDTO]:
        with get_sqlmodel_session(self.db_set) as session:
            return html_filters_to_dtos(
                session.exec(select(HtmlFilter).where(HtmlFilter.kind == "regex_filter", HtmlFilter.plus != "")).all()
            )

    def exists(self, html: str, kind: str) -> bool:
        with get_sqlmodel_session(self.db_set) as session:
            return cast(
                bool,
                session.exec(select(func.count()).select_from(HtmlFilter).where(HtmlFilter.html == html, HtmlFilter.kind == kind)).one() > 0,
            )

    def get(self, html: str, kind: str) -> HtmlFilterDTO | None:
        with get_sqlmodel_session(self.db_set) as session:
            return optional_html_filter_to_dto(session.get(HtmlFilter, (html, kind)))

    def get_by_kind_plus(self, kind: str, plus: str) -> HtmlFilterDTO | None:
        with get_sqlmodel_session(self.db_set) as session:
            return optional_html_filter_to_dto(session.exec(select(HtmlFilter).where(HtmlFilter.kind == kind, HtmlFilter.plus == plus).limit(1)).first())

    def get_plus_t(self, html: str, kind: str, *, default: str = "") -> str:
        with get_sqlmodel_session(self.db_set) as session:
            value = select(HtmlFilter.plus_t).where(
                HtmlFilter.html == html,
                HtmlFilter.kind == kind,
            )

            return cast(str, session.exec(select(func.coalesce(value.scalar_subquery(), default))).one())

    def upsert(self, html: str, kind: str, *, plus: str = "", plus_t: str = "") -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.merge(HtmlFilter(html=html, kind=kind, plus=plus, plus_t=plus_t))
            session.commit()

    def delete(self, html: str, kind: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(delete(HtmlFilter).where(col(HtmlFilter.html) == html, col(HtmlFilter.kind) == kind))
            session.commit()
