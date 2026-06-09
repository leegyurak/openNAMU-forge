import datetime
import hashlib
import json
import urllib.parse

import flask

from opennamu_forge.infrastructure.setting_repository import OtherSettingRepository
from opennamu_forge.infrastructure.user_setting_repository import UserSettingRepository

try:
    import orjson

    def json_dumps(obj):
        return orjson.dumps(obj).decode("utf-8")

    def json_loads(s):
        return orjson.loads(s if isinstance(s, bytes) else s.encode("utf-8"))
except ImportError:
    import json

    json_dumps = json.dumps
    json_loads = json.loads

try:
    import regex as re
except:
    import re

global_func_some_set = {}


def global_func_some_set_do(set_name, data=None):
    global global_func_some_set

    if data is not None:
        global_func_some_set[set_name] = data

    if set_name in global_func_some_set:
        return global_func_some_set[set_name]
    else:
        return None


def get_time():
    return str(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))


def db_change(data):
    set_data = global_func_some_set_do("db_type")
    if set_data == "mysql":
        data = data.replace("random()", "rand()")
        data = data.replace("%", "%%")
        data = data.replace("?", "%s")
        data = data.replace("collate nocase", "collate utf8mb4_general_ci")
    elif set_data == "postgresql":
        data = data.replace("random()", "random()")
        data = data.replace("collate nocase", "")
        data = re.sub(r'"([^"]*)"', lambda match: "'" + match.group(1).replace("'", "''") + "'", data)
        data = re.sub(r"\b([A-Za-z_][A-Za-z0-9_]*) \+ 0\b", r"CAST(\1 AS INTEGER)", data)
        data = data.replace("%", "%%")
        data = data.replace("?", "%s")
        data = re.sub(r"\blimit\s+%s\s*,\s*([0-9]+)", r"limit \1 offset %s", data, flags=re.I)

    return data


def _get_current_db_set():
    db_type = global_func_some_set_do("db_type")
    db_set = {
        "type": db_type,
        "name": global_func_some_set_do("db_name"),
    }

    if db_type == "mysql":
        db_set.update(
            {
                "mysql_host": global_func_some_set_do("db_mysql_host"),
                "mysql_user": global_func_some_set_do("db_mysql_user"),
                "mysql_pw": global_func_some_set_do("db_mysql_pw"),
                "mysql_port": global_func_some_set_do("db_mysql_port"),
            }
        )
    elif db_type == "postgresql":
        db_set.update(
            {
                "postgresql_host": global_func_some_set_do("db_postgresql_host"),
                "postgresql_user": global_func_some_set_do("db_postgresql_user"),
                "postgresql_pw": global_func_some_set_do("db_postgresql_pw"),
                "postgresql_port": global_func_some_set_do("db_postgresql_port"),
            }
        )

    return db_set


def ip_check(d_type=0):
    ip = "::1"
    if d_type == 0 and (flask.session and "id" in flask.session):
        ip = flask.session["id"]
    else:
        set_data = global_func_some_set_do("load_ip_select")
        if not set_data or set_data == "default":
            ip = flask.request.environ.get(
                "HTTP_X_REAL_IP",
                flask.request.environ.get("HTTP_CF_CONNECTING_IP", flask.request.environ.get("REMOTE_ADDR", "::1")),
            )
        else:
            ip = flask.request.environ.get(set_data, "::1")

        if ip_or_user(ip) == 0:
            ip = "::1"

    return ip


def ip_or_user(data=""):
    # without_DB

    # 1 == ip
    # 0 == reg

    if data == "":
        data = ip_check()

    if re.search(r"(\.|:)", data):
        return 1
    else:
        return 0


def url_pas(data):
    data = re.sub(r"^\.", "\\\\.", data)
    data = urllib.parse.quote(data)
    data = data.replace("/", "%2F")

    return data


def sha224_replace(data):
    return hashlib.sha224(bytes(data, "utf-8")).hexdigest()


def md5_replace(data):
    return hashlib.md5(data.encode()).hexdigest()


def get_main_skin_set(conn, flask_session, set_name, ip):
    other_settings = OtherSettingRepository(_get_current_db_set())
    user_settings = UserSettingRepository(_get_current_db_set())

    if ip_or_user(ip) == 0:
        set_data = user_settings.get(ip, set_name) or "default"
    else:
        set_data = flask_session[set_name] if set_name in flask_session and flask_session[set_name] != "" else "default"

    if set_data == "default":
        set_data = other_settings.get(set_name) or "default"

    return set_data
