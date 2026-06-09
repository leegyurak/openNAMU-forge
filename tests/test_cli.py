import sys
from types import SimpleNamespace

import pytest

from opennamu_forge import cli


def test_cli_parser는_dev_command를_파싱한다():
    args = cli.build_parser().parse_args(["dev"])

    assert args.command == "dev"


def test_cli_serve는_gunicorn으로_process를_교체한다(monkeypatch):
    exec_call = {}

    def fake_execvp(file_name, command):
        exec_call["file_name"] = file_name
        exec_call["command"] = command

    monkeypatch.setattr(cli.os, "execvp", fake_execvp)

    result = cli.main(["serve", "--host", "127.0.0.1", "--port", "4000", "--workers", "2", "--threads", "3"])

    assert result == 0
    assert exec_call["file_name"] == "gunicorn"
    assert exec_call["command"] == [
        "gunicorn",
        "--bind",
        "127.0.0.1:4000",
        "--workers",
        "2",
        "--threads",
        "3",
        "app:create_app()",
    ]


def test_cli_dev는_app_main을_dev_mode로_호출한다(monkeypatch):
    main_call = {}

    def fake_main():
        main_call["called"] = True

    monkeypatch.setitem(sys.modules, "app", SimpleNamespace(main=fake_main))
    monkeypatch.setattr(cli.sys, "argv", ["opennamu-forge"])

    assert cli.main(["dev"]) == 0
    assert cli.sys.argv == ["opennamu-forge", "dev"]
    assert main_call["called"] is True


def test_cli_migrate는_sqlmodel_db에서_alembic을_실행한다(monkeypatch):
    fake_engine = SimpleNamespace(dispose=lambda: None)
    migration_result = SimpleNamespace(engine=fake_engine, table_names={"data", "history"})
    migration_call = {}

    monkeypatch.setenv("NAMU_DB_TYPE", "sqlite")
    monkeypatch.setattr(cli, "load_env_file", lambda: None)

    def fake_run_schema_migrations(db_set):
        migration_call["db_set"] = db_set
        return migration_result

    monkeypatch.setattr(cli, "run_schema_migrations", fake_run_schema_migrations)

    assert cli.main(["migrate"]) == 0
    assert migration_call["db_set"]["type"] == "sqlite"


def test_cli_main은_지원하지_않는_command를_거부한다(monkeypatch):
    fake_parser = SimpleNamespace(parse_args=lambda argv: SimpleNamespace(command="unknown"))

    monkeypatch.setattr(cli, "build_parser", lambda: fake_parser)

    with pytest.raises(RuntimeError, match="Unsupported command"):
        cli.main(["unknown"])


def test_cli_migrate는_sqlmodel_미지원_db에서_migration을_건너뛴다(monkeypatch):
    monkeypatch.setenv("NAMU_DB_TYPE", "unsupported")
    monkeypatch.setattr(cli, "load_env_file", lambda: None)

    def fail_run_schema_migrations(db_set):
        raise AssertionError("migration should not run")

    monkeypatch.setattr(cli, "run_schema_migrations", fail_run_schema_migrations)

    assert cli.main(["migrate"]) == 0
