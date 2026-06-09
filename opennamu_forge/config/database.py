from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote_plus

from opennamu_forge.config.env import env_bool


@dataclass(frozen=True)
class SqlModelEngineConfig:
    pool_pre_ping: bool
    pool_size: int | None
    max_overflow: int | None
    pool_recycle: int | None
    pool_timeout: int | None


@dataclass(frozen=True)
class DatabaseConfig:
    type: str
    name: str
    mysql_host: str
    mysql_user: str
    mysql_pw: str
    mysql_port: str
    postgresql_host: str
    postgresql_user: str
    postgresql_pw: str
    postgresql_port: str

    def to_runtime_options(self) -> dict[str, str]:
        return {
            "type": self.type,
            "name": self.name,
            "mysql_host": self.mysql_host,
            "mysql_user": self.mysql_user,
            "mysql_pw": self.mysql_pw,
            "mysql_port": self.mysql_port,
            "postgresql_host": self.postgresql_host,
            "postgresql_user": self.postgresql_user,
            "postgresql_pw": self.postgresql_pw,
            "postgresql_port": self.postgresql_port,
        }


DatabaseConfigLike = DatabaseConfig | Mapping[str, Any]


def is_sqlmodel_database_type(db_config: DatabaseConfigLike) -> bool:
    return _db_value(db_config, "type") in {"sqlite", "mysql", "postgresql"}


def build_database_config_from_env(environ: Mapping[str, str] | None = None) -> DatabaseConfig:
    env = environ if environ is not None else os.environ
    db_type = env.get("NAMU_DB_TYPE", "sqlite").lower()
    normalized_db_type = "postgresql" if db_type == "postgres" else db_type

    return DatabaseConfig(
        type=normalized_db_type,
        name=env.get("NAMU_DB", "data"),
        mysql_host=env.get("NAMU_DB_HOST", "localhost"),
        mysql_user=env.get("NAMU_DB_USER", "root"),
        mysql_pw=env.get("NAMU_DB_PASSWORD", ""),
        mysql_port=env.get("NAMU_DB_PORT", "3306"),
        postgresql_host=env.get("NAMU_DB_HOST", "localhost"),
        postgresql_user=env.get("NAMU_DB_USER", "postgres"),
        postgresql_pw=env.get("NAMU_DB_PASSWORD", ""),
        postgresql_port=env.get("NAMU_DB_PORT", "5432"),
    )


def build_sqlmodel_database_url(db_config: DatabaseConfigLike) -> str:
    database_options = _database_options(db_config)
    db_type = database_options["type"]
    if db_type == "sqlite":
        return "sqlite:///" + database_options["name"] + ".db"
    if db_type == "mysql":
        return (
            "mysql+pymysql://"
            + quote_plus(database_options["mysql_user"])
            + ":"
            + quote_plus(database_options["mysql_pw"])
            + "@"
            + database_options["mysql_host"]
            + ":"
            + str(database_options["mysql_port"])
            + "/"
            + database_options["name"]
            + "?charset=utf8mb4"
        )
    if db_type == "postgresql":
        return (
            "postgresql+psycopg://"
            + quote_plus(database_options["postgresql_user"])
            + ":"
            + quote_plus(database_options["postgresql_pw"])
            + "@"
            + database_options["postgresql_host"]
            + ":"
            + str(database_options["postgresql_port"])
            + "/"
            + database_options["name"]
        )

    raise ValueError("Unsupported database type: " + str(db_type))


def build_sqlmodel_engine_config(db_config: DatabaseConfigLike) -> SqlModelEngineConfig:
    pool_enabled = _db_value(db_config, "type") != "sqlite"
    return SqlModelEngineConfig(
        pool_pre_ping=_env_bool("NAMU_DB_POOL_PRE_PING", default=pool_enabled),
        pool_size=_env_int("NAMU_DB_POOL_SIZE", default=5) if pool_enabled else None,
        max_overflow=_env_int("NAMU_DB_MAX_OVERFLOW", default=10) if pool_enabled else None,
        pool_recycle=_env_int("NAMU_DB_POOL_RECYCLE", default=3600) if pool_enabled else None,
        pool_timeout=_env_int("NAMU_DB_POOL_TIMEOUT", default=30) if pool_enabled else None,
    )


def _env_bool(name: str, *, default: bool) -> bool:
    return env_bool(os.environ, name, default=default)


def _env_int(name: str, *, default: int) -> int:
    return int(os.getenv(name, str(default)))


def _database_options(db_config: DatabaseConfigLike) -> Mapping[str, Any]:
    if isinstance(db_config, DatabaseConfig):
        return db_config.to_runtime_options()
    return db_config


def _db_value(db_config: DatabaseConfigLike, key: str) -> Any:
    return _database_options(db_config)[key]
