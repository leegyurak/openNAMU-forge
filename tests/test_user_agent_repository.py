from pathlib import Path

import pytest


@pytest.fixture()
def user_agent_db_set(tmp_path):
    from opennamu_forge.infrastructure.database_config import reset_sqlmodel_engine
    from opennamu_forge.infrastructure.db_model import UserAgentData, get_sqlmodel_session
    from opennamu_forge.infrastructure.migrations import run_schema_migrations

    db_set = {"type": "sqlite", "name": str(Path(tmp_path) / "user-agent")}
    reset_sqlmodel_engine()
    migration_result = run_schema_migrations(db_set)

    with get_sqlmodel_session(db_set) as session:
        session.add(UserAgentData(name="alpha", ip="10.0.0.1", ua="A", today="2026-01-02 00:00:00", sub=""))
        session.add(UserAgentData(name="beta", ip="10.0.0.1", ua="B", today="2026-01-01 00:00:00", sub=""))
        session.add(UserAgentData(name="alpha", ip="10.0.0.2", ua="C", today="2026-01-03 00:00:00", sub=""))
        session.commit()

    yield db_set

    migration_result.engine.dispose()
    reset_sqlmodel_engine()


def test_user_agent_repository는_identity별_distinct_ip를_센다(user_agent_db_set):
    from opennamu_forge.infrastructure.user_agent_repository import UserAgentDataRepository

    repository = UserAgentDataRepository(user_agent_db_set)

    assert repository.count_distinct_ips_by_identity("name", "alpha") == 2
    assert repository.count_distinct_ips_by_two_identities("name", "alpha", "name", "beta") == 2


def test_user_agent_repository는_identity별_record를_조회한다(user_agent_db_set):
    from opennamu_forge.infrastructure.user_agent_repository import UserAgentDataRepository

    repository = UserAgentDataRepository(user_agent_db_set)

    rows = repository.list_by_identity("name", "alpha")

    assert len(rows) == 2
    assert rows[0].ip == "10.0.0.2"
    assert rows[1].ip == "10.0.0.1"


def test_user_agent_repository는_두_identity_record를_조회한다(user_agent_db_set):
    from opennamu_forge.infrastructure.user_agent_repository import UserAgentDataRepository

    repository = UserAgentDataRepository(user_agent_db_set)

    rows = repository.list_by_two_identities("name", "alpha", "name", "beta")

    assert len(rows) == 3
    assert rows[0].name == "alpha"
    assert rows[2].name == "beta"


def test_user_agent_repository는_distinct_value를_조회한다(user_agent_db_set):
    from opennamu_forge.infrastructure.user_agent_repository import UserAgentDataRepository

    repository = UserAgentDataRepository(user_agent_db_set)

    rows = repository.list_distinct_values_by_identity("name", "ip", "10.0.0.1")

    assert rows == ["alpha", "beta"]


def test_user_agent_repository는_record를_삭제한다(user_agent_db_set):
    from opennamu_forge.infrastructure.user_agent_repository import UserAgentDataRepository

    repository = UserAgentDataRepository(user_agent_db_set)

    repository.delete("alpha", "10.0.0.2", "2026-01-03 00:00:00")

    assert repository.count_distinct_ips_by_identity("name", "alpha") == 1


def test_user_agent_repository는_record를_추가한다(user_agent_db_set):
    from opennamu_forge.infrastructure.user_agent_repository import UserAgentDataRepository

    repository = UserAgentDataRepository(user_agent_db_set)

    repository.add("gamma", "10.0.0.3", "D", "2026-01-04 00:00:00")

    assert repository.count_distinct_ips_by_identity("name", "gamma") == 1
