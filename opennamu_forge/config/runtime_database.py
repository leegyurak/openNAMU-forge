from __future__ import annotations

from typing import Any

from opennamu_forge.application.runtime_context import get_runtime_value, set_runtime_value


def apply_database_runtime_config(database_options: dict[str, str]) -> None:
    for name, value in database_options.items():
        set_runtime_value("db_" + name, value)


def get_current_database_runtime_options() -> dict[str, Any]:
    db_type = get_runtime_value("db_type")
    database_options = {
        "type": db_type,
        "name": get_runtime_value("db_name"),
    }

    if db_type == "mysql":
        database_options.update(
            {
                "mysql_host": get_runtime_value("db_mysql_host"),
                "mysql_user": get_runtime_value("db_mysql_user"),
                "mysql_pw": get_runtime_value("db_mysql_pw"),
                "mysql_port": get_runtime_value("db_mysql_port"),
            }
        )
    elif db_type == "postgresql":
        database_options.update(
            {
                "postgresql_host": get_runtime_value("db_postgresql_host"),
                "postgresql_user": get_runtime_value("db_postgresql_user"),
                "postgresql_pw": get_runtime_value("db_postgresql_pw"),
                "postgresql_port": get_runtime_value("db_postgresql_port"),
            }
        )

    return database_options
