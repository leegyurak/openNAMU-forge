from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from sqlalchemy import func, literal, or_
from sqlmodel import col, select

from opennamu_forge.infrastructure.db_model import WikiData, get_sqlmodel_session


@dataclass(frozen=True)
class WikiDocumentRepository:
    db_set: dict[str, str]

    def list_titles(
        self,
        *,
        exclude_user_pages: bool = False,
        exclude_file_pages: bool = False,
        exclude_category_pages: bool = False,
    ) -> list[str]:
        title_column = col(WikiData.title)
        query = (
            select(title_column)
            .where(
                or_(literal(not exclude_user_pages), title_column.not_like("user:%")),
                or_(literal(not exclude_file_pages), title_column.not_like("file:%")),
                or_(literal(not exclude_category_pages), title_column.not_like("category:%")),
            )
            .order_by(title_column)
        )

        with get_sqlmodel_session(self.db_set) as session:
            return cast(list[str], session.exec(query).all())

    def list_titles_page(self, *, offset: int = 0, limit: int = 50, prefix: str = "") -> list[str]:
        title_column = col(WikiData.title)
        query = select(title_column).where(title_column.like(prefix + "%")).order_by(title_column).offset(offset).limit(limit)

        with get_sqlmodel_session(self.db_set) as session:
            return cast(list[str], session.exec(query).all())

    def count_titles(self, *, prefix: str = "") -> int:
        title_column = col(WikiData.title)
        query = select(func.count()).select_from(WikiData).where(title_column.like(prefix + "%"))

        with get_sqlmodel_session(self.db_set) as session:
            return int(session.exec(query).one())
