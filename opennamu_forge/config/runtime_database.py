from __future__ import annotations

from typing import Any

from opennamu_forge.application.runtime_context import get_runtime_value, set_runtime_value


def apply_database_runtime_config(db_set: dict[str, str]) -> None:
    for name, value in db_set.items():
        set_runtime_value("db_" + name, value)


def get_current_db_set() -> dict[str, Any]:
    db_type = get_runtime_value("db_type")
    db_set = {
        "type": db_type,
        "name": get_runtime_value("db_name"),
    }

    if db_type == "mysql":
        db_set.update(
            {
                "mysql_host": get_runtime_value("db_mysql_host"),
                "mysql_user": get_runtime_value("db_mysql_user"),
                "mysql_pw": get_runtime_value("db_mysql_pw"),
                "mysql_port": get_runtime_value("db_mysql_port"),
            }
        )
    elif db_type == "postgresql":
        db_set.update(
            {
                "postgresql_host": get_runtime_value("db_postgresql_host"),
                "postgresql_user": get_runtime_value("db_postgresql_user"),
                "postgresql_pw": get_runtime_value("db_postgresql_pw"),
                "postgresql_port": get_runtime_value("db_postgresql_port"),
            }
        )

    return db_set
