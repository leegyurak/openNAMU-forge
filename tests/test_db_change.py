import importlib.util
from pathlib import Path

import pytest


@pytest.fixture
def func_tool():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "opennamu_forge"
        / "presentation"
        / "routes"
        / "tool"
        / "func_tool.py"
    )
    spec = importlib.util.spec_from_file_location("opennamu_forge_func_tool_for_test", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("opennamu_forge/presentation/routes/tool/func_tool.py 로드에 실패했습니다.")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.global_func_some_set.clear()
    return module


def test_sqlite_sql은_변경하지_않는다(func_tool):
    func_tool.global_func_some_set_do("db_type", "sqlite")

    sql = 'select data from other where name = "ver" and id = ?'

    assert func_tool.db_change(sql) == sql


def test_db_type이_없으면_sql은_변경하지_않는다(func_tool):
    sql = "select random() from data where title like ?"

    assert func_tool.db_change(sql) == sql


def test_mysql_sql은_mysql_placeholder와_collation을_사용한다(func_tool):
    func_tool.global_func_some_set_do("db_type", "mysql")

    sql = "select title from data where title like ? collate nocase limit 1"

    assert func_tool.db_change(sql) == "select title from data where title like %s collate utf8mb4_general_ci limit 1"


def test_mysql_sql은_random과_percent를_변환한다(func_tool):
    func_tool.global_func_some_set_do("db_type", "mysql")

    sql = "select random() from data where title like '%A%' and id = ?"

    assert func_tool.db_change(sql) == "select rand() from data where title like '%%A%%' and id = %s"


def test_postgresql_sql은_placeholder와_limit_offset을_변환한다(func_tool):
    func_tool.global_func_some_set_do("db_type", "postgresql")

    sql = "select id from history where title = ? order by id + 0 desc limit ?, 50"

    assert (
        func_tool.db_change(sql)
        == "select id from history where title = %s order by CAST(id AS INTEGER) desc limit 50 offset %s"
    )


def test_postgresql_sql은_큰따옴표_문자열을_변환한다(func_tool):
    func_tool.global_func_some_set_do("db_type", "postgresql")

    sql = 'select data from other where name = "ver"'

    assert func_tool.db_change(sql) == "select data from other where name = 'ver'"


def test_postgresql_sql은_문자열_내_작은따옴표를_escape한다(func_tool):
    func_tool.global_func_some_set_do("db_type", "postgresql")

    sql = 'select data from other where name = "owner\'s page"'

    assert func_tool.db_change(sql) == "select data from other where name = 'owner''s page'"


def test_postgresql_sql은_collate_nocase를_제거한다(func_tool):
    func_tool.global_func_some_set_do("db_type", "postgresql")

    sql = "select title from data where title like ? collate nocase"

    assert func_tool.db_change(sql) == "select title from data where title like %s "


def test_전역_설정은_저장하고_조회한다(func_tool):
    assert func_tool.global_func_some_set_do("missing") is None
    assert func_tool.global_func_some_set_do("db_type", "postgresql") == "postgresql"
    assert func_tool.global_func_some_set_do("db_type") == "postgresql"


def test_문자열_헬퍼는_기존_출력을_유지한다(func_tool):
    assert func_tool.url_pas("./A/B") == "%5C.%2FA%2FB"
    assert func_tool.sha224_replace("OpenNamu Forge") == "a80cdeda8410c42f471fe2eafa4c1fc66ab84a2634522591f4b74f2f"
    assert func_tool.md5_replace("OpenNamu Forge") == "741c396b18a6f4d87f84c382dcbe9a10"


def test_json_헬퍼는_직렬화와_역직렬화를_지원한다(func_tool):
    payload = {"name": "테스트", "count": 1}

    encoded = func_tool.json_dumps(payload)

    assert isinstance(encoded, str)
    assert func_tool.json_loads(encoded) == payload


def test_ip_or_user는_ip와_사용자를_구분한다(func_tool):
    assert func_tool.ip_or_user("127.0.0.1") == 1
    assert func_tool.ip_or_user("2001:db8::1") == 1
    assert func_tool.ip_or_user("wiki-user") == 0


def test_ip_check는_session_id를_우선한다(func_tool):
    app = func_tool.flask.Flask(__name__)
    app.secret_key = "test-secret"

    with app.test_request_context("/"):
        func_tool.flask.session["id"] = "login-user"

        assert func_tool.ip_check() == "login-user"


def test_ip_check는_header에서_ip를_읽는다(func_tool):
    app = func_tool.flask.Flask(__name__)
    app.secret_key = "test-secret"

    with app.test_request_context("/", environ_base={"HTTP_X_REAL_IP": "203.0.113.10"}):
        assert func_tool.ip_check() == "203.0.113.10"


def test_ip_check는_custom_header를_읽는다(func_tool):
    app = func_tool.flask.Flask(__name__)
    app.secret_key = "test-secret"
    func_tool.global_func_some_set_do("load_ip_select", "HTTP_X_FORWARDED_FOR")

    with app.test_request_context("/", environ_base={"HTTP_X_FORWARDED_FOR": "198.51.100.5"}):
        assert func_tool.ip_check() == "198.51.100.5"


def test_ip_check는_d_type이_0이_아니면_session_id를_사용하지_않는다(func_tool):
    app = func_tool.flask.Flask(__name__)
    app.secret_key = "test-secret"

    with app.test_request_context("/", environ_base={"REMOTE_ADDR": "198.51.100.7"}):
        func_tool.flask.session["id"] = "login-user"

        assert func_tool.ip_check(d_type=1) == "198.51.100.7"


def test_ip_check는_사용자형_헤더를_루프백으로_대체한다(func_tool):
    app = func_tool.flask.Flask(__name__)
    app.secret_key = "test-secret"

    with app.test_request_context("/", environ_base={"HTTP_X_REAL_IP": "wiki-user"}):
        assert func_tool.ip_check() == "::1"


class FakeCursor:
    def __init__(self, rows):
        self.rows = list(rows)
        self.executed = []

    def execute(self, sql, params):
        self.executed.append((sql, params))

    def fetchall(self):
        return self.rows.pop(0)


class FakeConnection:
    def __init__(self, rows):
        self.cursor_instance = FakeCursor(rows)

    def cursor(self):
        return self.cursor_instance


def test_main_skin_set은_사용자_설정을_우선한다(func_tool):
    conn = FakeConnection([[("ringo",)]])

    assert func_tool.get_main_skin_set(conn, {}, "main_skin", "wiki-user") == "ringo"
    assert conn.cursor_instance.executed == [
        ("select data from user_set where name = ? and id = ?", ["main_skin", "wiki-user"])
    ]


def test_main_skin_set은_기본값이면_공통_설정으로_fallback한다(func_tool):
    conn = FakeConnection([[("liberty",)]])

    assert func_tool.get_main_skin_set(conn, {}, "main_skin", "127.0.0.1") == "liberty"
    assert conn.cursor_instance.executed == [("select data from other where name = ?", ["main_skin"])]


def test_main_skin_set은_설정이_비어있으면_default를_반환한다(func_tool):
    conn = FakeConnection([[("",)], []])

    assert func_tool.get_main_skin_set(conn, {}, "main_skin", "wiki-user") == "default"
