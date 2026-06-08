from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote_plus

from sqlalchemy.engine import Engine
from sqlmodel import Session, create_engine


@dataclass(frozen=True)
class SqlModelEngineConfig:
    pool_pre_ping: bool
    pool_size: int | None
    max_overflow: int | None
    pool_recycle: int | None
    pool_timeout: int | None


_sqlmodel_engine: Engine | None = None


def build_sqlmodel_database_url(db_set: dict[str, Any]) -> str:
    db_type = db_set["type"]
    if db_type == "sqlite":
        return "sqlite:///" + db_set["name"] + ".db"
    if db_type == "mysql":
        return (
            "mysql+pymysql://"
            + quote_plus(db_set["mysql_user"])
            + ":"
            + quote_plus(db_set["mysql_pw"])
            + "@"
            + db_set["mysql_host"]
            + ":"
            + str(db_set["mysql_port"])
            + "/"
            + db_set["name"]
            + "?charset=utf8mb4"
        )
    if db_type == "postgresql":
        return (
            "postgresql+psycopg://"
            + quote_plus(db_set["postgresql_user"])
            + ":"
            + quote_plus(db_set["postgresql_pw"])
            + "@"
            + db_set["postgresql_host"]
            + ":"
            + str(db_set["postgresql_port"])
            + "/"
            + db_set["name"]
        )

    raise ValueError("Unsupported database type: " + str(db_type))


def build_sqlmodel_engine_config(db_set: dict[str, Any]) -> SqlModelEngineConfig:
    pool_enabled = db_set["type"] != "sqlite"
    return SqlModelEngineConfig(
        pool_pre_ping=_env_bool("NAMU_DB_POOL_PRE_PING", default=pool_enabled),
        pool_size=_env_int("NAMU_DB_POOL_SIZE", default=5) if pool_enabled else None,
        max_overflow=_env_int("NAMU_DB_MAX_OVERFLOW", default=10) if pool_enabled else None,
        pool_recycle=_env_int("NAMU_DB_POOL_RECYCLE", default=3600) if pool_enabled else None,
        pool_timeout=_env_int("NAMU_DB_POOL_TIMEOUT", default=30) if pool_enabled else None,
    )


def get_sqlmodel_engine(db_set: dict[str, Any]) -> Engine:
    global _sqlmodel_engine

    if _sqlmodel_engine is None:
        _sqlmodel_engine = create_engine(
            build_sqlmodel_database_url(db_set),
            **build_sqlmodel_create_engine_kwargs(db_set),
        )

    return _sqlmodel_engine


def build_sqlmodel_create_engine_kwargs(db_set: dict[str, Any]) -> dict[str, Any]:
    config = build_sqlmodel_engine_config(db_set)
    kwargs: dict[str, Any] = {
        "connect_args": {"check_same_thread": False} if db_set["type"] == "sqlite" else {},
        "pool_pre_ping": config.pool_pre_ping,
    }
    _set_optional(kwargs, "pool_size", config.pool_size)
    _set_optional(kwargs, "max_overflow", config.max_overflow)
    _set_optional(kwargs, "pool_recycle", config.pool_recycle)
    _set_optional(kwargs, "pool_timeout", config.pool_timeout)
    return kwargs


def reset_sqlmodel_engine() -> None:
    global _sqlmodel_engine

    if _sqlmodel_engine is not None:
        _sqlmodel_engine.dispose()
    _sqlmodel_engine = None


def open_sqlmodel_session(db_set: dict[str, Any]) -> Session:
    return Session(get_sqlmodel_engine(db_set))


def _set_optional(target: dict[str, Any], key: str, value: Any | None) -> None:
    if value is not None:
        target[key] = value


def _env_bool(name: str, *, default: bool) -> bool:
    return os.getenv(name, str(default)).lower() in {"1", "true", "yes", "on"}


def _env_int(name: str, *, default: int) -> int:
    return int(os.getenv(name, str(default)))
