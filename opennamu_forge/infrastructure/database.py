from __future__ import annotations

import os
from collections.abc import Mapping
from typing import Any


def should_init_sqlmodel(db_set: dict[str, Any]) -> bool:
    return db_set["type"] in {"sqlite", "mysql", "postgresql"}


def build_database_settings_from_env(environ: Mapping[str, str] | None = None) -> dict[str, str]:
    env = environ if environ is not None else os.environ
    db_type = env.get("NAMU_DB_TYPE", "sqlite").lower()
    normalized_db_type = "postgresql" if db_type == "postgres" else db_type

    return {
        "type": normalized_db_type,
        "name": env.get("NAMU_DB", "data"),
        "mysql_host": env.get("NAMU_DB_HOST", "localhost"),
        "mysql_user": env.get("NAMU_DB_USER", "root"),
        "mysql_pw": env.get("NAMU_DB_PASSWORD", ""),
        "mysql_port": env.get("NAMU_DB_PORT", "3306"),
        "postgresql_host": env.get("NAMU_DB_HOST", "localhost"),
        "postgresql_user": env.get("NAMU_DB_USER", "postgres"),
        "postgresql_pw": env.get("NAMU_DB_PASSWORD", ""),
        "postgresql_port": env.get("NAMU_DB_PORT", "5432"),
    }
