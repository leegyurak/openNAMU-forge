from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from sqlalchemy import Integer, delete, func, update
from sqlalchemy import cast as sa_cast
from sqlmodel import col, select

from opennamu_forge.application.dto.vote import VoteDTO
from opennamu_forge.infrastructure.db_model import Vote, get_sqlmodel_session
from opennamu_forge.infrastructure.mappers.vote_mapper import optional_vote_to_dto, votes_to_dtos


@dataclass(frozen=True)
class VoteRepository:
    db_set: dict[str, str]

    def latest_vote_id(self) -> int | None:
        with get_sqlmodel_session(self.db_set) as session:
            return session.exec(select(func.max(sa_cast(col(Vote.id), Integer))).where(Vote.user == "")).first()

    def add_main(self, name: str, vote_id: str, subject: str, data: str, vote_type: str, acl: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.add(Vote(name=name, id=vote_id, subject=subject, data=data, user="", type=vote_type, acl=acl))
            session.commit()

    def add_option(self, name: str, vote_id: str, data: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.add(Vote(name=name, id=vote_id, subject="", data=data, user="", type="option", acl=""))
            session.commit()

    def add_selection(self, vote_id: str, data: str, user: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.add(Vote(name="", id=vote_id, subject="", data=data, user=user, type="select", acl=""))
            session.commit()

    def list_by_types(self, vote_types: tuple[str, ...], *, offset: int = 0, limit: int = 50) -> list[VoteDTO]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(
                select(Vote)
                .where(
                    Vote.user == "",
                    col(Vote.type).in_(vote_types),
                )
                .offset(offset)
                .limit(limit)
            ).all()

            return votes_to_dtos(rows)

    def get_main(self, vote_id: str) -> VoteDTO | None:
        with get_sqlmodel_session(self.db_set) as session:
            return optional_vote_to_dto(
                session.exec(
                    select(Vote).where(
                        Vote.id == vote_id,
                        Vote.user == "",
                        col(Vote.type).in_(("open", "n_open", "close", "n_close")),
                    )
                ).first()
            )

    def get_option(self, vote_id: str, name: str, *, default: str = "") -> str:
        with get_sqlmodel_session(self.db_set) as session:
            value = select(Vote.data).where(
                Vote.id == vote_id,
                Vote.name == name,
                Vote.type == "option",
            )

            return cast(str, session.exec(select(func.coalesce(value.scalar_subquery(), default))).one())

    def has_user_selection(self, vote_id: str, user: str) -> bool:
        with get_sqlmodel_session(self.db_set) as session:
            return cast(bool, session.exec(select(func.count()).select_from(Vote).where(Vote.id == vote_id, Vote.user == user)).one() > 0)

    def list_selection_users(self, vote_id: str, data: str) -> list[str]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(col(Vote.user)).where(Vote.id == vote_id, Vote.user != "", Vote.data == data)).all()

            return cast(list[str], rows)

    def update_main_type(self, vote_id: str, old_type: str, new_type: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(update(Vote).where(col(Vote.user) == "", col(Vote.id) == vote_id, col(Vote.type) == old_type).values(type=new_type))
            session.commit()

    def delete_option(self, vote_id: str, name: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(delete(Vote).where(col(Vote.id) == vote_id, col(Vote.name) == name, col(Vote.type) == "option"))
            session.commit()
