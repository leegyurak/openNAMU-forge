from pathlib import Path

import pytest


@pytest.fixture()
def admin_db_set(tmp_path):
    from opennamu_forge.infrastructure.database_config import reset_sqlmodel_engine
    from opennamu_forge.infrastructure.db_model import AdminList, AdminRecord, get_sqlmodel_session
    from opennamu_forge.infrastructure.migrations import run_schema_migrations

    db_set = {"type": "sqlite", "name": str(Path(tmp_path) / "admin")}
    reset_sqlmodel_engine()
    migration_result = run_schema_migrations(db_set)

    with get_sqlmodel_session(db_set) as session:
        session.add(AdminList(name="owner", acl="owner"))
        session.add(AdminList(name="admin", acl="ban"))
        session.add(AdminRecord(who="tester", what="ban user", time="2026-01-02 00:00:00"))
        session.add(AdminRecord(who="tester", what="acl edit", time="2026-01-01 00:00:00"))
        session.commit()

    yield db_set

    migration_result.engine.dispose()
    reset_sqlmodel_engine()


def test_admin_repository는_group_name을_조회한다(admin_db_set):
    from opennamu_forge.infrastructure.admin_repository import AdminRepository

    repository = AdminRepository(admin_db_set)

    assert repository.list_group_names() == ["admin", "owner"]


def test_admin_repository는_group_acl을_교체한다(admin_db_set):
    from opennamu_forge.infrastructure.admin_repository import AdminRepository

    repository = AdminRepository(admin_db_set)

    repository.set_group_acls("admin", ("ban", "acl", "nothing"))

    assert repository.list_group_acls("admin") == ["acl", "ban", "nothing"]


def test_admin_repository는_group을_삭제한다(admin_db_set):
    from opennamu_forge.infrastructure.admin_repository import AdminRepository

    repository = AdminRepository(admin_db_set)

    repository.delete_group("admin")

    assert repository.list_group_acls("admin") == []


def test_admin_repository는_record를_조회한다(admin_db_set):
    from opennamu_forge.infrastructure.admin_repository import AdminRepository

    repository = AdminRepository(admin_db_set)

    records = repository.list_records()

    assert records[0].action == "ban user"
    assert records[1].action == "acl edit"


def test_admin_repository는_record_prefix를_적용한다(admin_db_set):
    from opennamu_forge.infrastructure.admin_repository import AdminRepository

    repository = AdminRepository(admin_db_set)

    records = repository.list_records(action_prefix="ban")

    assert len(records) == 1
    assert records[0].action == "ban user"
    assert repository.count_records(action_prefix="ban") == 1


def test_admin_repository는_latest_record_time을_조회한다(admin_db_set):
    from opennamu_forge.infrastructure.admin_repository import AdminRepository

    repository = AdminRepository(admin_db_set)

    assert repository.latest_record_time(action_prefix="ban") == "2026-01-02 00:00:00"
    assert repository.latest_record_time(action_prefix="missing", default="fallback") == "fallback"
