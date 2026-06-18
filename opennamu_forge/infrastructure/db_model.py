from contextlib import contextmanager
from typing import Any

from sqlalchemy import Column, String, Text
from sqlmodel import Field, SQLModel

from opennamu_forge.infrastructure.database_engine import get_sqlmodel_engine, open_sqlmodel_session


def _text_column() -> Column[Any]:
    return Column(Text, nullable=False)


def _pk_text_column() -> Column[Any]:
    return Column(String(191), primary_key=True, nullable=False, server_default="")


class BaseRow(SQLModel):
    pass


class DataSet(BaseRow, table=True):
    __tablename__ = "data_set"
    __table_args__ = {"extend_existing": True}

    doc_name: str = Field(default="", sa_column=_pk_text_column())
    doc_rev: str = Field(default="", sa_column=_pk_text_column())
    set_name: str = Field(default="", sa_column=_pk_text_column())
    set_data: str = Field(default="", sa_column=_text_column())


class WikiData(BaseRow, table=True):
    __tablename__ = "data"
    __table_args__ = {"extend_existing": True}

    title: str = Field(default="", sa_column=_pk_text_column())
    data: str = Field(default="", sa_column=_text_column())
    type: str = Field(default="", sa_column=_text_column())


class History(BaseRow, table=True):
    __tablename__ = "history"
    __table_args__ = {"extend_existing": True}

    id: str = Field(default="", sa_column=_pk_text_column())
    title: str = Field(default="", sa_column=_pk_text_column())
    data: str = Field(default="", sa_column=_text_column())
    date: str = Field(default="", sa_column=_text_column())
    ip: str = Field(default="", sa_column=_text_column())
    send: str = Field(default="", sa_column=_text_column())
    leng: str = Field(default="", sa_column=_text_column())
    hide: str = Field(default="", sa_column=_text_column())
    type: str = Field(default="", sa_column=_text_column())


class RecentChange(BaseRow, table=True):
    __tablename__ = "rc"
    __table_args__ = {"extend_existing": True}

    id: str = Field(default="", sa_column=_pk_text_column())
    title: str = Field(default="", sa_column=_pk_text_column())
    date: str = Field(default="", sa_column=_text_column())
    type: str = Field(default="", sa_column=_text_column())


class Acl(BaseRow, table=True):
    __tablename__ = "acl"
    __table_args__ = {"extend_existing": True}

    title: str = Field(default="", sa_column=_pk_text_column())
    data: str = Field(default="", sa_column=_text_column())
    type: str = Field(default="", sa_column=_pk_text_column())


class Backlink(BaseRow, table=True):
    __tablename__ = "back"
    __table_args__ = {"extend_existing": True}

    title: str = Field(default="", sa_column=_pk_text_column())
    link: str = Field(default="", sa_column=_pk_text_column())
    type: str = Field(default="", sa_column=_pk_text_column())
    data: str = Field(default="", sa_column=_text_column())


class TopicSet(BaseRow, table=True):
    __tablename__ = "topic_set"
    __table_args__ = {"extend_existing": True}

    thread_code: str = Field(default="", sa_column=_pk_text_column())
    set_name: str = Field(default="", sa_column=_pk_text_column())
    set_id: str = Field(default="", sa_column=_pk_text_column())
    set_data: str = Field(default="", sa_column=_text_column())


class RecentDiscuss(BaseRow, table=True):
    __tablename__ = "rd"
    __table_args__ = {"extend_existing": True}

    title: str = Field(default="", sa_column=_pk_text_column())
    sub: str = Field(default="", sa_column=_pk_text_column())
    code: str = Field(default="", sa_column=_pk_text_column())
    date: str = Field(default="", sa_column=_text_column())
    band: str = Field(default="", sa_column=_text_column())
    stop: str = Field(default="", sa_column=_text_column())
    agree: str = Field(default="", sa_column=_text_column())
    acl: str = Field(default="", sa_column=_text_column())


class Topic(BaseRow, table=True):
    __tablename__ = "topic"
    __table_args__ = {"extend_existing": True}

    id: str = Field(default="", sa_column=_pk_text_column())
    data: str = Field(default="", sa_column=_text_column())
    date: str = Field(default="", sa_column=_text_column())
    ip: str = Field(default="", sa_column=_text_column())
    block: str = Field(default="", sa_column=_text_column())
    top: str = Field(default="", sa_column=_text_column())
    code: str = Field(default="", sa_column=_pk_text_column())


class RecentBlock(BaseRow, table=True):
    __tablename__ = "rb"
    __table_args__ = {"extend_existing": True}

    block: str = Field(default="", sa_column=_pk_text_column())
    end: str = Field(default="", sa_column=_text_column())
    today: str = Field(default="", sa_column=_pk_text_column())
    blocker: str = Field(default="", sa_column=_text_column())
    why: str = Field(default="", sa_column=_text_column())
    band: str = Field(default="", sa_column=_text_column())
    login: str = Field(default="", sa_column=_text_column())
    ongoing: str = Field(default="", sa_column=_text_column())


class Other(BaseRow, table=True):
    __tablename__ = "other"
    __table_args__ = {"extend_existing": True}

    name: str = Field(default="", sa_column=_pk_text_column())
    data: str = Field(default="", sa_column=_text_column())
    coverage: str = Field(default="", sa_column=_pk_text_column())


class HtmlFilter(BaseRow, table=True):
    __tablename__ = "html_filter"
    __table_args__ = {"extend_existing": True}

    html: str = Field(default="", sa_column=_pk_text_column())
    kind: str = Field(default="", sa_column=_pk_text_column())
    plus: str = Field(default="", sa_column=_text_column())
    plus_t: str = Field(default="", sa_column=_text_column())


class Vote(BaseRow, table=True):
    __tablename__ = "vote"
    __table_args__ = {"extend_existing": True}

    name: str = Field(default="", sa_column=_pk_text_column())
    id: str = Field(default="", sa_column=_pk_text_column())
    subject: str = Field(default="", sa_column=_text_column())
    data: str = Field(default="", sa_column=_text_column())
    user: str = Field(default="", sa_column=_pk_text_column())
    type: str = Field(default="", sa_column=_pk_text_column())
    acl: str = Field(default="", sa_column=_text_column())


class AdminList(BaseRow, table=True):
    __tablename__ = "alist"
    __table_args__ = {"extend_existing": True}

    name: str = Field(default="", sa_column=_pk_text_column())
    acl: str = Field(default="", sa_column=_pk_text_column())


class AdminRecord(BaseRow, table=True):
    __tablename__ = "re_admin"
    __table_args__ = {"extend_existing": True}

    who: str = Field(default="", sa_column=_pk_text_column())
    what: str = Field(default="", sa_column=_pk_text_column())
    time: str = Field(default="", sa_column=_pk_text_column())


class UserAgentData(BaseRow, table=True):
    __tablename__ = "ua_d"
    __table_args__ = {"extend_existing": True}

    name: str = Field(default="", sa_column=_pk_text_column())
    ip: str = Field(default="", sa_column=_pk_text_column())
    ua: str = Field(default="", sa_column=_pk_text_column())
    today: str = Field(default="", sa_column=_pk_text_column())
    sub: str = Field(default="", sa_column=_text_column())


class UserSet(BaseRow, table=True):
    __tablename__ = "user_set"
    __table_args__ = {"extend_existing": True}

    name: str = Field(default="", sa_column=_pk_text_column())
    id: str = Field(default="", sa_column=_pk_text_column())
    data: str = Field(default="", sa_column=_text_column())


class UserNotice(BaseRow, table=True):
    __tablename__ = "user_notice"
    __table_args__ = {"extend_existing": True}

    id: str = Field(default="", sa_column=_pk_text_column())
    name: str = Field(default="", sa_column=_pk_text_column())
    data: str = Field(default="", sa_column=_text_column())
    date: str = Field(default="", sa_column=_text_column())
    readme: str = Field(default="", sa_column=_text_column())


class BbsSet(BaseRow, table=True):
    __tablename__ = "bbs_set"
    __table_args__ = {"extend_existing": True}

    set_name: str = Field(default="", sa_column=_pk_text_column())
    set_code: str = Field(default="", sa_column=_pk_text_column())
    set_id: str = Field(default="", sa_column=_pk_text_column())
    set_data: str = Field(default="", sa_column=_text_column())


class BbsData(BaseRow, table=True):
    __tablename__ = "bbs_data"
    __table_args__ = {"extend_existing": True}

    set_name: str = Field(default="", sa_column=_pk_text_column())
    set_code: str = Field(default="", sa_column=_pk_text_column())
    set_id: str = Field(default="", sa_column=_pk_text_column())
    set_data: str = Field(default="", sa_column=_text_column())


def init_sqlmodel(db_set):
    engine = get_sqlmodel_engine(db_set)
    SQLModel.metadata.create_all(engine)
    return engine


@contextmanager
def get_sqlmodel_session(db_set):
    with open_sqlmodel_session(db_set) as session:
        yield session
