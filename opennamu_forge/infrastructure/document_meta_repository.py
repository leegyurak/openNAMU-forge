from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from sqlalchemy import delete, func, update
from sqlmodel import col, select

from opennamu_forge.infrastructure.db_model import Acl, DataSet, get_sqlmodel_session


@dataclass(frozen=True)
class DocumentMetaRepository:
    db_set: dict[str, str]

    def get(self, doc_name: str, set_name: str, *, doc_rev: str = "", default: str = "") -> str:
        with get_sqlmodel_session(self.db_set) as session:
            value = select(DataSet.set_data).where(
                DataSet.doc_name == doc_name,
                DataSet.doc_rev == doc_rev,
                DataSet.set_name == set_name,
            )

            return cast(str, session.exec(select(func.coalesce(value.scalar_subquery(), default))).one())

    def list_no_link_documents(self, *, offset: int = 0, limit: int = 50) -> list[tuple[str, str]]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(
                select(col(DataSet.doc_name), col(DataSet.set_data))
                .where(
                    DataSet.doc_rev == "",
                    DataSet.set_name == "link_count",
                    DataSet.set_data == "0",
                )
                .offset(offset)
                .limit(limit)
            ).all()

            return cast(list[tuple[str, str]], rows)

    def rename_doc_name(self, old_name: str, new_name: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(update(DataSet).where(col(DataSet.doc_name) == old_name).values(doc_name=new_name))
            session.commit()

    def delete_doc_name(self, doc_name: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(delete(DataSet).where(col(DataSet.doc_name) == doc_name))
            session.commit()

    def rename_acl_title(self, old_title: str, new_title: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(update(Acl).where(col(Acl.title) == old_title).values(title=new_title))
            session.commit()

    def delete_acl_title(self, title: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(delete(Acl).where(col(Acl.title) == title))
            session.commit()
