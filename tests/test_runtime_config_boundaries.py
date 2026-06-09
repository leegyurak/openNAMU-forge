import pytest

from opennamu_forge.application.runtime_context import clear_runtime_context, get_runtime_value
from opennamu_forge.config.runtime_database import apply_database_runtime_config, get_current_db_set
from opennamu_forge.config.startup_options import get_init_set_list


@pytest.fixture(autouse=True)
def test_runtime_context를_초기화한다():
    clear_runtime_context()
    yield
    clear_runtime_context()


@pytest.mark.parametrize(
    ("db_set", "expected"),
    [
        (
            {"type": "sqlite", "name": "data"},
            {"type": "sqlite", "name": "data"},
        ),
        (
            {
                "type": "mysql",
                "name": "wiki",
                "mysql_host": "mysql",
                "mysql_user": "root",
                "mysql_pw": "pw",
                "mysql_port": "3306",
            },
            {
                "type": "mysql",
                "name": "wiki",
                "mysql_host": "mysql",
                "mysql_user": "root",
                "mysql_pw": "pw",
                "mysql_port": "3306",
            },
        ),
        (
            {
                "type": "postgresql",
                "name": "wiki",
                "postgresql_host": "postgres",
                "postgresql_user": "forge",
                "postgresql_pw": "pw",
                "postgresql_port": "5432",
            },
            {
                "type": "postgresql",
                "name": "wiki",
                "postgresql_host": "postgres",
                "postgresql_user": "forge",
                "postgresql_pw": "pw",
                "postgresql_port": "5432",
            },
        ),
    ],
)
def test_database_runtime_config는_runtime_context에_저장된다(db_set, expected):
    apply_database_runtime_config(db_set)

    assert get_current_db_set() == expected


def test_database_runtime_config는_db_prefix로_저장된다():
    apply_database_runtime_config({"type": "sqlite", "name": "data"})

    assert get_runtime_value("db_type") == "sqlite"
    assert get_runtime_value("db_name") == "data"


def test_startup_options는_전체_옵션을_반환한다():
    options = get_init_set_list()

    assert options["host"]["default"] == "0.0.0.0"
    assert options["language"]["list"] == ["ko-KR", "en-US"]
    assert options["markup"]["default"] == "namumark"


def test_startup_options는_개별_옵션을_반환한다():
    option = get_init_set_list("markup")

    assert option["require"] == "select"
    assert option["list"] == ["namumark", "namumark_beta", "macromark", "markdown", "custom", "raw"]


def test_startup_options는_없는_옵션이면_key_error를_낸다():
    with pytest.raises(KeyError):
        get_init_set_list("missing")
