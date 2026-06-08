from __future__ import annotations

import argparse
import os
import sys

from opennamu_forge.infrastructure.database import build_database_settings_from_env, should_init_sqlmodel
from opennamu_forge.infrastructure.env import load_env_file
from opennamu_forge.infrastructure.logging import get_logger
from opennamu_forge.infrastructure.migrations import run_schema_migrations

logger = get_logger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="opennamu-forge")
    subcommands = parser.add_subparsers(dest="command", required=True)

    subcommands.add_parser("dev", help="Run the Flask development server.")
    subcommands.add_parser("migrate", help="Run Alembic migrations for the configured database.")

    serve_parser = subcommands.add_parser("serve", help="Run Gunicorn with the configured WSGI factory.")
    serve_parser.add_argument("--host", default=os.getenv("NAMU_HOST", "0.0.0.0"))
    serve_parser.add_argument("--port", default=os.getenv("NAMU_PORT", "3000"))
    serve_parser.add_argument("--workers", default=os.getenv("NAMU_GUNICORN_WORKERS", "1"))
    serve_parser.add_argument("--threads", default=os.getenv("NAMU_GUNICORN_THREADS", "1"))

    return parser


def run_dev() -> int:
    sys.argv = [sys.argv[0], "dev"]

    from app import main as app_main

    app_main()
    return 0


def run_migrate() -> int:
    load_env_file()
    db_set = build_database_settings_from_env()

    if not should_init_sqlmodel(db_set):
        logger.info("Alembic migrations are not enabled for DB type: %s", db_set["type"])
        return 0

    result = run_schema_migrations(db_set)
    logger.info("Alembic migration completed. table_count=%d", len(result.table_names))
    result.engine.dispose()
    return 0


def run_serve(args: argparse.Namespace) -> int:
    bind = args.host + ":" + args.port
    command = [
        "gunicorn",
        "--bind",
        bind,
        "--workers",
        args.workers,
        "--threads",
        args.threads,
        "app:create_app()",
    ]
    os.execvp(command[0], command)
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "dev":
        return run_dev()
    if args.command == "migrate":
        return run_migrate()
    if args.command == "serve":
        return run_serve(args)

    raise RuntimeError("Unsupported command: " + str(args.command))


if __name__ == "__main__":
    raise SystemExit(main())
