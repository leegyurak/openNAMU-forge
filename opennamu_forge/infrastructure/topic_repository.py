from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from sqlalchemy import Integer, case, delete, func, update
from sqlalchemy import cast as sa_cast
from sqlmodel import col, select

from opennamu_forge.application.dto.discussion import RecentDiscussDTO, TopicCommentDTO
from opennamu_forge.infrastructure.db_model import RecentDiscuss, Topic, TopicSet, get_sqlmodel_session
from opennamu_forge.infrastructure.mappers.topic_mapper import (
    optional_recent_discuss_to_dto,
    optional_topic_to_dto,
    topics_to_dtos,
)


@dataclass(frozen=True)
class TopicRepository:
    db_set: dict[str, str]

    def get(self, code: str, comment_id: str) -> TopicCommentDTO | None:
        with get_sqlmodel_session(self.db_set) as session:
            return optional_topic_to_dto(
                session.exec(
                    select(Topic).where(
                        Topic.code == code,
                        Topic.id == comment_id,
                    )
                )
                .first()
            )

    def list_by_ip(self, ip: str, *, offset: int = 0, limit: int = 50) -> list[TopicCommentDTO]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(
                select(Topic)
                .where(Topic.ip == ip)
                .order_by(col(Topic.date).desc())
                .offset(offset)
                .limit(limit)
            ).all()

            return topics_to_dtos(rows)

    def get_recent_discuss(self, code: str) -> RecentDiscussDTO | None:
        with get_sqlmodel_session(self.db_set) as session:
            return optional_recent_discuss_to_dto(session.exec(select(RecentDiscuss).where(RecentDiscuss.code == code)).first())

    def get_thread_setting(self, code: str, name: str, *, default: str = "") -> str:
        with get_sqlmodel_session(self.db_set) as session:
            value = select(TopicSet.set_data).where(
                TopicSet.thread_code == code,
                TopicSet.set_name == name,
            )

            return cast(str, session.exec(select(func.coalesce(value.scalar_subquery(), default))).one())

    def latest_topic_code(self) -> int | None:
        with get_sqlmodel_session(self.db_set) as session:
            return session.exec(select(func.max(sa_cast(col(Topic.code), Integer)))).first()

    def latest_comment_id(self, code: str) -> int | None:
        with get_sqlmodel_session(self.db_set) as session:
            return session.exec(select(func.max(sa_cast(col(Topic.id), Integer))).where(Topic.code == code)).first()

    def add_comment(self, code: str, comment_id: str, data: str, date: str, ip: str, block: str, *, top: str = "") -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.add(Topic(code=code, id=comment_id, data=data, date=date, ip=ip, block=block, top=top))
            session.commit()

    def list_comment_ids_ascending(self, code: str) -> list[str]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(col(Topic.id)).where(Topic.code == code).order_by(sa_cast(col(Topic.id), Integer).asc())).all()

            return cast(list[str], rows)

    def first_comment_author(self, code: str) -> str | None:
        with get_sqlmodel_session(self.db_set) as session:
            return session.exec(select(Topic.ip).where(Topic.code == code, Topic.id == "1").limit(1)).first()

    def update_recent_discuss_acl(self, code: str, acl: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(update(RecentDiscuss).where(col(RecentDiscuss.code) == code).values(acl=acl))
            session.commit()

    def upsert_thread_setting(self, code: str, name: str, data: str, *, set_id: str = "1") -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(delete(TopicSet).where(col(TopicSet.thread_code) == code, col(TopicSet.set_name) == name))
            session.add(TopicSet(thread_code=code, set_name=name, set_id=set_id, set_data=data))
            session.commit()

    def toggle_top(self, code: str, comment_id: str) -> bool:
        with get_sqlmodel_session(self.db_set) as session:
            result = session.exec(
                update(Topic)
                .where(
                    col(Topic.code) == code,
                    col(Topic.id) == comment_id,
                )
                .values(top=case((col(Topic.top) == "O", ""), else_="O"))
            )
            session.commit()
            return result.rowcount > 0

    def toggle_block(self, code: str, comment_id: str) -> bool:
        with get_sqlmodel_session(self.db_set) as session:
            result = session.exec(
                update(Topic)
                .where(
                    col(Topic.code) == code,
                    col(Topic.id) == comment_id,
                )
                .values(block=case((col(Topic.block) == "O", ""), else_="O"))
            )
            session.commit()
            return result.rowcount > 0

    def delete(self, code: str, comment_id: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(
                delete(Topic).where(
                    col(Topic.code) == code,
                    col(Topic.id) == comment_id,
                )
            )
            session.commit()

    def delete_thread(self, code: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(delete(Topic).where(col(Topic.code) == code))
            session.exec(delete(RecentDiscuss).where(col(RecentDiscuss.code) == code))
            session.commit()

    def update_recent_discuss_title_subtitle(self, code: str, title: str, subtitle: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(update(RecentDiscuss).where(col(RecentDiscuss.code) == code).values(title=title, sub=subtitle))
            session.commit()

    def update_recent_discuss_stop(self, code: str, stop: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(update(RecentDiscuss).where(col(RecentDiscuss.code) == code).values(stop=stop))
            session.commit()

    def update_recent_discuss_agree(self, code: str, agree: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(update(RecentDiscuss).where(col(RecentDiscuss.code) == code).values(agree=agree))
            session.commit()

    def update_recent_discuss_date(self, code: str, date: str) -> bool:
        with get_sqlmodel_session(self.db_set) as session:
            result = session.exec(update(RecentDiscuss).where(col(RecentDiscuss.code) == code).values(date=date))
            session.commit()
            return result.rowcount > 0

    def add_recent_discuss(self, code: str, title: str, subtitle: str, date: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.add(RecentDiscuss(code=code, title=title, sub=subtitle, date=date, band="", stop="", agree="", acl=""))
            session.commit()

    def exists_recent_discuss_title(self, title: str) -> bool:
        with get_sqlmodel_session(self.db_set) as session:
            return cast(bool, session.exec(select(func.count()).select_from(RecentDiscuss).where(RecentDiscuss.title == title)).one() > 0)

    def exists_open_recent_discuss_title(self, title: str) -> bool:
        with get_sqlmodel_session(self.db_set) as session:
            return cast(
                bool,
                session.exec(select(func.count()).select_from(RecentDiscuss).where(RecentDiscuss.title == title, RecentDiscuss.stop != "O")).one() > 0,
            )

    def rename_recent_discuss_title(self, old_title: str, new_title: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(update(RecentDiscuss).where(col(RecentDiscuss.title) == old_title).values(title=new_title))
            session.commit()

    def count_by_ip(self, ip: str) -> int:
        with get_sqlmodel_session(self.db_set) as session:
            return int(session.exec(select(func.count()).select_from(Topic).where(Topic.ip == ip)).one())

    def latest_date_by_ip(self, ip: str) -> str | None:
        with get_sqlmodel_session(self.db_set) as session:
            return session.exec(select(Topic.date).where(Topic.ip == ip).order_by(col(Topic.date).desc()).limit(1)).first()
