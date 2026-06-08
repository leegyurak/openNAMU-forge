import os

from opennamu_forge.infrastructure.env import env_bool, load_env_file, parse_env_line


def test_env_line은_key_value를_파싱한다():
    assert parse_env_line("NAMU_DB_TYPE=postgresql") == ("NAMU_DB_TYPE", "postgresql")
    assert parse_env_line("export NAMU_DB=data") == ("NAMU_DB", "data")
    assert parse_env_line('NAMU_DB_PASSWORD="pass # word"') == ("NAMU_DB_PASSWORD", "pass # word")
    assert parse_env_line("NAMU_DB_USER='open namu'") == ("NAMU_DB_USER", "open namu")
    assert parse_env_line("NAMU_DB_HOST=db # comment") == ("NAMU_DB_HOST", "db")
    assert parse_env_line(" NAMU_DB_PORT = 5432 ") == ("NAMU_DB_PORT", "5432")


def test_env_line은_빈줄과_주석을_무시한다():
    assert parse_env_line("") is None
    assert parse_env_line("# comment") is None
    assert parse_env_line("not-a-key-value") is None
    assert parse_env_line("=empty-key") is None


def test_env_file은_기존_환경변수를_기본적으로_덮어쓰지_않는다(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("NAMU_DB_TYPE=postgresql\nNAMU_DB=data\n", encoding="utf-8")
    monkeypatch.setenv("NAMU_DB_TYPE", "sqlite")
    monkeypatch.delenv("NAMU_DB", raising=False)

    assert load_env_file(env_file) is True
    assert env_bool({"NAMU_PROMETHEUS_ENABLED": "true"}, "NAMU_PROMETHEUS_ENABLED", default=False) is True
    assert os.environ["NAMU_DB_TYPE"] == "sqlite"
    assert os.environ["NAMU_DB"] == "data"


def test_env_file은_export와_주석과_잘못된_라인을_함께_처리한다(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "# comment",
                "export NAMU_DB_TYPE=postgresql",
                "invalid",
                "NAMU_DB_HOST=db # comment",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.delenv("NAMU_DB_TYPE", raising=False)
    monkeypatch.delenv("NAMU_DB_HOST", raising=False)

    assert load_env_file(env_file) is True
    assert os.environ["NAMU_DB_TYPE"] == "postgresql"
    assert os.environ["NAMU_DB_HOST"] == "db"


def test_env_file은_override가_true이면_덮어쓴다(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("NAMU_DB_TYPE=postgresql\n", encoding="utf-8")
    monkeypatch.setenv("NAMU_DB_TYPE", "sqlite")

    assert load_env_file(env_file, override=True) is True
    assert os.environ["NAMU_DB_TYPE"] == "postgresql"


def test_env_file이_없으면_false를_반환한다(tmp_path):
    assert load_env_file(tmp_path / ".env") is False


def test_env_bool은_일반적인_boolean_표현을_지원한다():
    assert env_bool({"A": "yes"}, "A", default=False) is True
    assert env_bool({"A": "1"}, "A", default=False) is True
    assert env_bool({"A": "ON"}, "A", default=False) is True
    assert env_bool({"A": "off"}, "A", default=True) is False
    assert env_bool({"A": "0"}, "A", default=True) is False
    assert env_bool({"A": "FALSE"}, "A", default=True) is False
    assert env_bool({"A": "unknown"}, "A", default=True) is True
    assert env_bool({}, "A", default=False) is False
