from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from sqlalchemy import func
from sqlmodel import col, select

from opennamu_forge.infrastructure.db_model import DataSet, get_sqlmodel_session


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
