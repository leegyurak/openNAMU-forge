from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from sqlalchemy import delete, func, update
from sqlmodel import col, select

from opennamu_forge.application.dto.document_meta import AclEntryDTO
from opennamu_forge.infrastructure.db_model import Acl, DataSet, get_sqlmodel_session
from opennamu_forge.infrastructure.mappers.document_meta_mapper import acl_entries_to_dtos


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

    def exists(self, doc_name: str, set_name: str, *, doc_rev: str = "") -> bool:
        with get_sqlmodel_session(self.db_set) as session:
            return cast(
                bool,
                session.exec(
                    select(func.count()).select_from(DataSet).where(
                        DataSet.doc_name == doc_name,
                        DataSet.doc_rev == doc_rev,
                        DataSet.set_name == set_name,
                    )
                ).one()
                > 0,
            )

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

    def list_doc_rev_data_by_set_name(self, set_name: str) -> list[tuple[str, str, str]]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(col(DataSet.doc_name), col(DataSet.doc_rev), col(DataSet.set_data)).where(DataSet.set_name == set_name)).all()

            return cast(list[tuple[str, str, str]], rows)

    def upsert(self, doc_name: str, set_name: str, set_data: str, *, doc_rev: str = "") -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.merge(DataSet(doc_name=doc_name, doc_rev=doc_rev, set_name=set_name, set_data=set_data))
            session.commit()

    def delete(self, doc_name: str, set_name: str, *, doc_rev: str = "") -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(
                delete(DataSet).where(
                    col(DataSet.doc_name) == doc_name,
                    col(DataSet.doc_rev) == doc_rev,
                    col(DataSet.set_name) == set_name,
                )
            )
            session.commit()

    def update_revision_marker(self, doc_name: str, doc_rev: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(
                update(DataSet)
                .where(
                    col(DataSet.doc_name) == doc_name,
                    col(DataSet.doc_rev).in_(("", "not_exist")),
                )
                .values(doc_rev=doc_rev)
            )
            session.commit()

    def get_acl(self, title: str, acl_type: str, *, default: str = "") -> str:
        with get_sqlmodel_session(self.db_set) as session:
            value = select(Acl.data).where(
                Acl.title == title,
                Acl.type == acl_type,
            )

            return cast(str, session.exec(select(func.coalesce(value.scalar_subquery(), default))).one())

    def acl_title_exists(self, title: str) -> bool:
        with get_sqlmodel_session(self.db_set) as session:
            return cast(bool, session.exec(select(func.count()).select_from(Acl).where(Acl.title == title)).one() > 0)

    def list_acl_entries(self, *, offset: int = 0, limit: int = 50) -> list[AclEntryDTO]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(
                select(Acl)
                .where(
                    Acl.data != "",
                    col(Acl.title).not_like("user:%"),
                )
                .order_by(col(Acl.title).desc())
                .offset(offset)
                .limit(limit)
            ).all()

            return acl_entries_to_dtos(rows)

    def upsert_acl(self, title: str, acl_type: str, data: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.merge(Acl(title=title, type=acl_type, data=data))
            session.commit()

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

    def delete_acl(self, title: str, acl_type: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(delete(Acl).where(col(Acl.title) == title, col(Acl.type) == acl_type))
            session.commit()
