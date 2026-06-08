from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from alembic import command
from alembic.config import Config
from sqlalchemy import inspect
from sqlalchemy.engine import Engine

from opennamu_forge.infrastructure.db_model import get_sqlmodel_database_url, get_sqlmodel_engine

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ALEMBIC_CONFIG_PATH = PROJECT_ROOT / "alembic.ini"
ALEMBIC_SCRIPT_LOCATION = PROJECT_ROOT / "migrations"


@dataclass(frozen=True)
class SchemaMigrationResult:
    engine: Engine
    table_names: set[str]


def build_alembic_config(database_url: str, config_path: Path = ALEMBIC_CONFIG_PATH) -> Config:
    config = Config(str(config_path))
    config.set_main_option("script_location", str(ALEMBIC_SCRIPT_LOCATION))
    config.set_main_option("sqlalchemy.url", database_url.replace("%", "%%"))
    return config


def run_schema_migrations(db_set: dict[str, Any]) -> SchemaMigrationResult:
    command.upgrade(build_alembic_config(get_sqlmodel_database_url(db_set)), "head")
    engine = get_sqlmodel_engine(db_set)
    return SchemaMigrationResult(
        engine=engine,
        table_names=set(inspect(engine).get_table_names()),
    )
