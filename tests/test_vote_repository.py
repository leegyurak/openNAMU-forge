from pathlib import Path

import pytest


@pytest.fixture()
def vote_db_set(tmp_path):
    from opennamu_forge.infrastructure.database_engine import reset_sqlmodel_engine
    from opennamu_forge.infrastructure.db_model import Vote, get_sqlmodel_session
    from opennamu_forge.infrastructure.migrations import run_schema_migrations

    db_set = {"type": "sqlite", "name": str(Path(tmp_path) / "vote")}
    reset_sqlmodel_engine()
    migration_result = run_schema_migrations(db_set)

    with get_sqlmodel_session(db_set) as session:
        session.add(Vote(name="Vote One", id="1", subject="subject", data="A\nB", user="", type="open", acl=""))
        session.add(Vote(name="open_user", id="1", subject="", data="tester", user="", type="option", acl=""))
        session.add(Vote(name="end_date", id="1", subject="", data="2026-01-01", user="", type="option", acl=""))
        session.add(Vote(name="Closed", id="2", subject="", data="A\nB", user="", type="close", acl=""))
        session.add(Vote(name="", id="1", subject="", data="0", user="alpha", type="select", acl=""))
        session.commit()

    yield db_set

    migration_result.engine.dispose()
    reset_sqlmodel_engine()


def test_vote_repository는_latest_vote_id를_조회한다(vote_db_set):
    from opennamu_forge.infrastructure.vote_repository import VoteRepository

    repository = VoteRepository(vote_db_set)

    assert repository.latest_vote_id() == 2


def test_vote_repository는_vote를_생성한다(vote_db_set):
    from opennamu_forge.infrastructure.vote_repository import VoteRepository

    repository = VoteRepository(vote_db_set)

    repository.add_main("Vote Three", "3", "subject", "A\nB", "n_open", "member")
    repository.add_option("open_user", "3", "tester")

    vote = repository.get_main("3")
    assert vote is not None
    assert vote.name == "Vote Three"
    assert vote.acl == "member"
    assert repository.get_option("3", "open_user") == "tester"


def test_vote_repository는_type별_vote를_조회한다(vote_db_set):
    from opennamu_forge.infrastructure.vote_repository import VoteRepository

    repository = VoteRepository(vote_db_set)

    open_votes = repository.list_by_types(("open", "n_open"))
    closed_votes = repository.list_by_types(("close", "n_close"))

    assert len(open_votes) == 1
    assert open_votes[0].vote_id == "1"
    assert len(closed_votes) == 1
    assert closed_votes[0].vote_id == "2"


def test_vote_repository는_user_selection을_관리한다(vote_db_set):
    from opennamu_forge.infrastructure.vote_repository import VoteRepository

    repository = VoteRepository(vote_db_set)

    repository.add_selection("1", "1", "beta")

    users_for_zero = repository.list_selection_users("1", "0")
    users_for_one = repository.list_selection_users("1", "1")

    assert repository.has_user_selection("1", "alpha") is True
    assert repository.has_user_selection("1", "missing") is False
    assert len(users_for_zero) == 1
    assert users_for_zero[0] == "alpha"
    assert len(users_for_one) == 1
    assert users_for_one[0] == "beta"


def test_vote_repository는_main_type과_option을_수정한다(vote_db_set):
    from opennamu_forge.infrastructure.vote_repository import VoteRepository

    repository = VoteRepository(vote_db_set)

    repository.update_main_type("1", "open", "close")
    repository.delete_option("1", "end_date")

    vote = repository.get_main("1")
    assert vote is not None
    assert vote.type == "close"
    assert repository.get_option("1", "end_date") == ""
