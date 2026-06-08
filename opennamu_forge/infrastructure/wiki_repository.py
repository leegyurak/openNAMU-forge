from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from sqlalchemy import delete, func, insert, literal, or_, update
from sqlmodel import col, select

from opennamu_forge.infrastructure.db_model import Backlink, WikiData, get_sqlmodel_session


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

    def get_data(self, title: str, *, default: str = "") -> str:
        with get_sqlmodel_session(self.db_set) as session:
            value = select(WikiData.data).where(WikiData.title == title)

            return cast(str, session.exec(select(func.coalesce(value.scalar_subquery(), default))).one())

    def exists_title(self, title: str) -> bool:
        with get_sqlmodel_session(self.db_set) as session:
            return cast(bool, session.exec(select(func.count()).select_from(WikiData).where(WikiData.title == title)).one() > 0)

    def delete_title(self, title: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(delete(WikiData).where(col(WikiData.title) == title))
            session.commit()

    def rename_title(self, old_title: str, new_title: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(update(WikiData).where(col(WikiData.title) == old_title).values(title=new_title))
            session.commit()

    def delete_backlinks_by_link(self, link: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(delete(Backlink).where(col(Backlink.link) == link))
            session.commit()

    def rename_backlink_link(self, old_link: str, new_link: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(update(Backlink).where(col(Backlink.link) == old_link).values(link=new_link))
            session.commit()

    def insert_no_backlinks_for_title(self, title: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(
                insert(Backlink).from_select(
                    ["link", "title", "type", "data"],
                    select(col(Backlink.link), literal(title), literal("no"), literal(""))
                    .where(Backlink.title == title)
                    .distinct(),
                )
            )
            session.commit()

    def delete_no_backlinks_for_title(self, title: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(delete(Backlink).where(col(Backlink.title) == title, col(Backlink.type) == "no"))
            session.commit()
