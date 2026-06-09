from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from sqlalchemy import delete, func, or_
from sqlmodel import col, select

from opennamu_forge.infrastructure.db_model import Backlink, get_sqlmodel_session
from opennamu_forge.infrastructure.mappers.backlink_mapper import backlink_rows_to_models


@dataclass(frozen=True)
class BacklinkRepository:
    db_set: dict[str, str]

    def list_distinct_refs(
        self,
        value_column: str,
        filter_column: str,
        filter_value: str,
        *,
        offset: int = 0,
        limit: int = 50,
    ) -> list[tuple[str, str]]:
        with get_sqlmodel_session(self.db_set) as session:
            value = getattr(Backlink, value_column)
            filter_value_column = getattr(Backlink, filter_column)
            rows = session.exec(
                select(value, col(Backlink.type))
                .where(
                    filter_value_column == filter_value,
                    Backlink.type != "no",
                    Backlink.type != "nothing",
                )
                .distinct()
                .order_by(col(Backlink.type).asc(), value.asc())
                .offset(offset)
                .limit(limit)
            ).all()

            return cast(list[tuple[str, str]], rows)

    def list_distinct_refs_case_insensitive(
        self,
        value_column: str,
        filter_column: str,
        filter_value: str,
        *,
        offset: int = 0,
        limit: int = 50,
    ) -> list[tuple[str, str]]:
        with get_sqlmodel_session(self.db_set) as session:
            value = getattr(Backlink, value_column)
            filter_value_column = getattr(Backlink, filter_column)
            rows = session.exec(
                select(value, col(Backlink.type))
                .where(
                    func.lower(filter_value_column) == filter_value.lower(),
                    Backlink.type != "no",
                    Backlink.type != "nothing",
                )
                .distinct()
                .order_by(col(Backlink.type).asc(), value.asc())
                .offset(offset)
                .limit(limit)
            ).all()

            return cast(list[tuple[str, str]], rows)

    def list_distinct_links_by_title_type(self, title: str, link_type: str) -> list[str]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(
                select(col(Backlink.link))
                .where(Backlink.title == title, Backlink.type == link_type)
                .distinct()
                .order_by(col(Backlink.link).asc())
            ).all()

            return cast(list[str], rows)

    def get_data(self, title: str, link: str, link_type: str, *, default: str = "") -> str:
        with get_sqlmodel_session(self.db_set) as session:
            value = select(Backlink.data).where(
                Backlink.title == title,
                Backlink.link == link,
                Backlink.type == link_type,
            )

            return cast(str, session.exec(select(func.coalesce(value.scalar_subquery(), default))).one())

    def exists(self, title: str, link: str, link_type: str) -> bool:
        with get_sqlmodel_session(self.db_set) as session:
            return cast(
                bool,
                session.exec(
                    select(func.count()).select_from(Backlink).where(
                        Backlink.title == title,
                        Backlink.link == link,
                        Backlink.type == link_type,
                    )
                ).one()
                > 0,
            )

    def has_include_title(self, title: str) -> bool:
        with get_sqlmodel_session(self.db_set) as session:
            return cast(
                bool,
                session.exec(select(func.count()).select_from(Backlink).where(Backlink.title == title, Backlink.type == "include")).one() > 0,
            )

    def get_redirect_for_link(self, link: str) -> tuple[str, str] | None:
        with get_sqlmodel_session(self.db_set) as session:
            return session.exec(select(Backlink.title, Backlink.data).where(Backlink.link == link, Backlink.type == "redirect").limit(1)).first()

    def redirect_exists_for_title_or_link(self, value: str) -> bool:
        with get_sqlmodel_session(self.db_set) as session:
            return cast(
                bool,
                session.exec(
                    select(func.count()).select_from(Backlink).where(
                        or_(col(Backlink.title) == value, col(Backlink.link) == value),
                        Backlink.type == "redirect",
                    )
                ).one()
                > 0,
            )

    def replace_for_document(self, doc_name: str, rows: list[tuple[str, str, str, str]]) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(delete(Backlink).where(col(Backlink.link) == doc_name))
            session.exec(delete(Backlink).where(col(Backlink.title) == doc_name, col(Backlink.type) == "no"))
            session.add_all(backlink_rows_to_models(rows))
            session.exec(delete(Backlink).where(col(Backlink.title) == doc_name, col(Backlink.type) == "no"))
            session.commit()
