import pytest


def test_sqlite_engine_config는_pool_옵션을_비활성화한다(monkeypatch):
    from opennamu_forge.infrastructure.database_engine import build_sqlmodel_create_engine_kwargs

    monkeypatch.delenv("NAMU_DB_POOL_SIZE", raising=False)

    kwargs = build_sqlmodel_create_engine_kwargs({"type": "sqlite", "name": "data"})

    assert kwargs == {
        "connect_args": {"check_same_thread": False},
        "pool_pre_ping": False,
    }


@pytest.mark.parametrize(
    ("env_name", "expected_key", "expected_value"),
    [
        ("NAMU_DB_POOL_SIZE", "pool_size", 7),
        ("NAMU_DB_MAX_OVERFLOW", "max_overflow", 11),
        ("NAMU_DB_POOL_RECYCLE", "pool_recycle", 120),
        ("NAMU_DB_POOL_TIMEOUT", "pool_timeout", 9),
    ],
)
def test_network_db_engine_config는_env_pool_옵션을_반영한다(monkeypatch, env_name, expected_key, expected_value):
    from opennamu_forge.infrastructure.database_engine import build_sqlmodel_create_engine_kwargs

    monkeypatch.setenv(env_name, str(expected_value))

    kwargs = build_sqlmodel_create_engine_kwargs({"type": "postgresql"})

    assert kwargs[expected_key] == expected_value


def test_network_db_engine_config는_pre_ping을_env로_끌_수_있다(monkeypatch):
    from opennamu_forge.infrastructure.database_engine import build_sqlmodel_create_engine_kwargs

    monkeypatch.setenv("NAMU_DB_POOL_PRE_PING", "false")

    kwargs = build_sqlmodel_create_engine_kwargs({"type": "mysql"})

    assert kwargs["pool_pre_ping"] is False
