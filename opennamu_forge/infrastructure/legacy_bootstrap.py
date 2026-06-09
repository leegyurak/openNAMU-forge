from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Any, cast

from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import Column, MetaData, Table, Text, column, delete, distinct, inspect, select, table, update
from sqlalchemy.schema import CreateIndex, DropIndex, Index
from sqlmodel import col

from opennamu_forge.infrastructure.database_config import get_sqlmodel_engine
from opennamu_forge.infrastructure.db_model import (
    Acl,
    Backlink,
    DataSet,
    History,
    HtmlFilter,
    Other,
    RecentBlock,
    RecentDiscuss,
    UserNotice,
    UserSet,
    WikiData,
    get_sqlmodel_session,
)


def _legacy_table(name: str, *columns: str):
    return table(name, *map(column, columns))


@dataclass(frozen=True)
class LegacyBootstrapAdapter:
    db_set: dict[str, str]

    def ensure_mysql_database(self, conn: Any, database_name: str) -> None:
        curs = conn.cursor()
        try:
            curs.execute("create database " + database_name + " default character set utf8mb4")
        except Exception:
            try:
                curs.execute("alter database " + database_name + " character set utf8mb4")
            except Exception:
                pass

    def set_sqlite_wal_journal(self, conn: Any) -> None:
        conn.execute("pragma journal_mode = WAL")

    def ensure_legacy_schema(self, conn: Any, tables: dict[str, list[str]], db_type: str) -> None:
        engine = get_sqlmodel_engine(self.db_set)
        for create_table in tables:
            column_names = ["test"] + tables[create_table]
            legacy_table = Table(create_table, MetaData(), *(Column(column_name, Text) for column_name in column_names))
            legacy_table.create(engine, checkfirst=True)

            existing_columns = {column_data["name"] for column_data in inspect(engine).get_columns(create_table)}
            with engine.begin() as connection:
                operations = Operations(MigrationContext.configure(connection))
                for column_name in column_names:
                    if column_name not in existing_columns:
                        try:
                            operations.add_column(create_table, Column(column_name, Text, server_default=""))
                        except Exception:
                            operations.add_column(create_table, Column(column_name, Text))

    def create_history_index_if_missing(self, conn: Any) -> None:
        history_table = Table("history", MetaData(), Column("title", Text), Column("ip", Text))
        Index("history_index", history_table.c.title, history_table.c.ip).create(get_sqlmodel_engine(self.db_set), checkfirst=True)

    def list_old_topic_first_rows(self) -> list[tuple[str, str, str]]:
        old_topic = _legacy_table("topic", "title", "sub", "code", "id")
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(old_topic.c.title, old_topic.c.sub, old_topic.c.code).where(old_topic.c.id == "1")).all()

            return cast(list[tuple[str, str, str]], rows)

    def update_old_topic_code(self, title: str, subtitle: str, code: str) -> None:
        old_topic = _legacy_table("topic", "title", "sub", "code")
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(update(old_topic).where(old_topic.c.title == title, old_topic.c.sub == subtitle).values(code=code))
            session.exec(update(RecentDiscuss).where(col(RecentDiscuss.title) == title, col(RecentDiscuss.sub) == subtitle).values(code=code))
            session.commit()

    def list_legacy_ban_regex_blocks(self) -> list[str]:
        legacy_ban = _legacy_table("ban", "block", "band")
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(legacy_ban.c.block).where(legacy_ban.c.band == "O")).all()

            return cast(list[str], rows)

    def convert_legacy_ban_regex_block(self, old_block: str, new_block: str) -> None:
        legacy_ban = _legacy_table("ban", "block", "band")
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(update(legacy_ban).where(legacy_ban.c.block == old_block, legacy_ban.c.band == "O").values(block=new_block, band="regex"))
            session.commit()

    def list_recent_block_regex_blocks(self) -> list[str]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(col(RecentBlock.block)).where(col(RecentBlock.band) == "O")).all()

            return cast(list[str], rows)

    def convert_recent_block_regex_block(self, old_block: str, new_block: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(update(RecentBlock).where(col(RecentBlock.block) == old_block, col(RecentBlock.band) == "O").values(block=new_block, band="regex"))
            session.commit()

    def list_legacy_bans(self) -> list[tuple[str, str, str, str, str]]:
        legacy_ban = _legacy_table("ban", "block", "end", "why", "band", "login")
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(legacy_ban.c.block, legacy_ban.c.end, legacy_ban.c.why, legacy_ban.c.band, legacy_ban.c.login)).all()

            return cast(list[tuple[str, str, str, str, str]], rows)

    def list_recent_history_rows_excluding_user(self, *, limit: int = 50) -> list[tuple[str, str, str]]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(
                select(col(History.id), col(History.title), col(History.date))
                .where(col(History.title).not_like("user:%"))
                .order_by(col(History.date).desc())
                .limit(limit)
            ).all()

            return cast(list[tuple[str, str, str]], rows)

    def list_legacy_filters(self) -> list[tuple[str, str, str]]:
        legacy_filter = _legacy_table("filter", "name", "regex", "sub")
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(legacy_filter.c.name, legacy_filter.c.regex, legacy_filter.c.sub)).all()

            return cast(list[tuple[str, str, str]], rows)

    def list_legacy_interwiki(self) -> list[tuple[str, str, str]]:
        legacy_inter = _legacy_table("inter", "title", "link", "icon")
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(legacy_inter.c.title, legacy_inter.c.link, legacy_inter.c.icon)).all()

            return cast(list[tuple[str, str, str]], rows)

    def list_legacy_custom_css(self) -> list[tuple[str, str]]:
        legacy_custom = _legacy_table("custom", "user", "css")
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(legacy_custom.c.user, legacy_custom.c.css)).all()

            return cast(list[tuple[str, str]], rows)

    def list_legacy_acl_rows(self) -> list[tuple[str, str, str, str, str]]:
        legacy_acl = _legacy_table("acl", "title", "decu", "dis", "view", "why")
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(legacy_acl.c.title, legacy_acl.c.decu, legacy_acl.c.dis, legacy_acl.c.view, legacy_acl.c.why)).all()

            return cast(list[tuple[str, str, str, str, str]], rows)

    def clear_legacy_cache(self) -> None:
        legacy_cache = _legacy_table("cache_data", "name")
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(delete(legacy_cache))
            session.commit()

    def delete_null_regex_filters(self) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(delete(HtmlFilter).where(col(HtmlFilter.kind) == "regex_filter", col(HtmlFilter.html).is_(None)))
            session.commit()

    def list_legacy_users(self) -> list[tuple[str, str, str, str, str]]:
        legacy_user = _legacy_table("user", "id", "pw", "acl", "date", "encode")
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(legacy_user.c.id, legacy_user.c.pw, legacy_user.c.acl, legacy_user.c.date, legacy_user.c.encode)).all()

            return cast(list[tuple[str, str, str, str, str]], rows)

    def list_legacy_user_applications(self) -> list[tuple[str, str, str, str, str, str, str, str, str]]:
        legacy_application = _legacy_table("user_application", "id", "pw", "date", "encode", "question", "answer", "ip", "ua", "email")
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(
                select(
                    legacy_application.c.id,
                    legacy_application.c.pw,
                    legacy_application.c.date,
                    legacy_application.c.encode,
                    legacy_application.c.question,
                    legacy_application.c.answer,
                    legacy_application.c.ip,
                    legacy_application.c.ua,
                    legacy_application.c.email,
                )
            ).all()

            return cast(list[tuple[str, str, str, str, str, str, str, str, str]], rows)

    def delete_file_admin_decu_acl(self) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(delete(Acl).where(col(Acl.title).like("file:%"), col(Acl.data) == "admin", col(Acl.type).like("decu%")))
            session.commit()

    def normalize_nulls(self, tables: dict[str, list[str]]) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            deque(
                (
                    session.exec(update(_legacy_table(table_name, column_name)).values({column_name: ""}).where(getattr(_legacy_table(table_name, column_name).c, column_name).is_(None)))
                    for table_name, column_names in tables.items()
                    for column_name in column_names
                ),
                maxlen=0,
            )
            session.commit()

    def clear_legacy_alarm(self) -> None:
        legacy_alarm = _legacy_table("alarm", "name")
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(delete(legacy_alarm))
            session.commit()

    def normalize_other_coverage(self) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(update(Other).where(col(Other.coverage).is_(None)).values(coverage=""))
            session.commit()

    def rebuild_history_index(self) -> None:
        history_table = Table("history", MetaData(), Column("title", Text), Column("ip", Text))
        history_index = Index("history_index", history_table.c.title, history_table.c.ip)
        with get_sqlmodel_session(self.db_set) as session:
            session.execute(DropIndex(history_index))
            session.execute(CreateIndex(history_index))
            session.commit()

    def clear_last_edit_meta(self) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(delete(DataSet).where(col(DataSet.set_name) == "last_edit"))
            session.commit()

    def latest_history_date_by_title(self, title: str) -> str | None:
        with get_sqlmodel_session(self.db_set) as session:
            return session.exec(select(col(History.date)).where(col(History.title) == title).order_by(col(History.date).desc()).limit(1)).first()

    def list_email_user_ids(self) -> list[str]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(col(UserSet.id)).where(col(UserSet.name) == "email")).all()

            return cast(list[str], rows)

    def normalize_backlink_data(self) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(update(Backlink).where(col(Backlink.data).is_(None)).values(data=""))
            session.commit()

    def clear_user_notices(self) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(delete(UserNotice))
            session.commit()

    def list_legacy_alarms(self) -> list[tuple[str, str, str]]:
        legacy_alarm = _legacy_table("alarm", "name", "data", "date")
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(legacy_alarm.c.name, legacy_alarm.c.data, legacy_alarm.c.date)).all()

            return cast(list[tuple[str, str, str]], rows)

    def add_user_notice(self, notice_id: str, user_id: str, data: str, date: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.add(UserNotice(id=notice_id, name=user_id, data=data, date=date, readme=""))
            session.commit()

    def list_application_settings(self) -> list[tuple[str, str, str]]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(col(UserSet.name), col(UserSet.id), col(UserSet.data)).where(col(UserSet.name) == "application")).all()

            return cast(list[tuple[str, str, str]], rows)

    def delete_application_settings(self) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(delete(UserSet).where(col(UserSet.name) == "application"))
            session.commit()

    def normalize_recent_block_nullable_columns(self) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(update(RecentBlock).where(col(RecentBlock.ongoing).is_(None)).values(ongoing=""))
            session.exec(update(RecentBlock).where(col(RecentBlock.login).is_(None)).values(login=""))
            session.commit()

    def list_legacy_scan_rows(self) -> list[tuple[str, str, str]]:
        legacy_scan = _legacy_table("scan", "title", "type", "user")
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(legacy_scan.c.title, legacy_scan.c.type, legacy_scan.c.user)).all()

            return cast(list[tuple[str, str, str]], rows)

    def list_edit_request_meta(self) -> list[tuple[str, str]]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(col(DataSet.doc_name), col(DataSet.doc_rev)).where(col(DataSet.set_name) == "edit_request_data")).all()

            return cast(list[tuple[str, str]], rows)

    def list_special_titles(self) -> list[str]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(
                select(col(WikiData.title)).where(
                    col(WikiData.title).like("category:%") | col(WikiData.title).like("user:%") | col(WikiData.title).like("file:%")
                )
            ).all()

            return cast(list[str], rows)

    def list_document_meta_names_with_revision_marker(self) -> list[str]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(distinct(col(DataSet.doc_name))).where(col(DataSet.doc_rev).in_(("not_exist", "")))).all()

            return cast(list[str], rows)

    def normalize_user_title_checkmark(self) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(update(UserSet).where(col(UserSet.name) == "user_title", col(UserSet.data) == "✅").values(data="☑️"))
            session.commit()

    def set_sqlite_delete_journal(self, conn: Any) -> None:
        conn.execute("pragma journal_mode = delete")

    def list_owner_acl_group_names(self) -> list[str]:
        admin_list = _legacy_table("alist", "name", "acl")
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(distinct(admin_list.c.name)).where(admin_list.c.acl == "owner")).all()

            return cast(list[str], rows)

    def list_user_ids_by_acl(self, acl_name: str) -> list[str]:
        with get_sqlmodel_session(self.db_set) as session:
            rows = session.exec(select(distinct(col(UserSet.id))).where(col(UserSet.name) == "acl", col(UserSet.data) == acl_name)).all()

            return cast(list[str], rows)
