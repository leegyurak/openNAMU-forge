from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from sqlalchemy.engine import Engine
from sqlmodel import Session, create_engine

from opennamu_forge.config.database import (
    DatabaseConfig,
    build_sqlmodel_database_url,
    build_sqlmodel_engine_config,
)

_sqlmodel_engine: Engine | None = None
DatabaseConfigLike = DatabaseConfig | Mapping[str, Any]


def get_sqlmodel_engine(db_set: DatabaseConfigLike) -> Engine:
    global _sqlmodel_engine

    if _sqlmodel_engine is None:
        _sqlmodel_engine = create_engine(
            build_sqlmodel_database_url(db_set),
            **build_sqlmodel_create_engine_kwargs(db_set),
        )

    return _sqlmodel_engine


def build_sqlmodel_create_engine_kwargs(db_set: DatabaseConfigLike) -> dict[str, Any]:
    config = build_sqlmodel_engine_config(db_set)
    kwargs: dict[str, Any] = {
        "connect_args": {"check_same_thread": False} if _db_type(db_set) == "sqlite" else {},
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


def open_sqlmodel_session(db_set: DatabaseConfigLike) -> Session:
    return Session(get_sqlmodel_engine(db_set))


def _set_optional(target: dict[str, Any], key: str, value: Any | None) -> None:
    if value is not None:
        target[key] = value


def _db_type(db_set: DatabaseConfigLike) -> str:
    if isinstance(db_set, DatabaseConfig):
        return db_set.type
    return str(db_set["type"])
