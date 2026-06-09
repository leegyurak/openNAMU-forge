import datetime
import hashlib
import importlib
import importlib.util
import json
import re as stdlib_re
import urllib.parse
from typing import Any

import flask

from opennamu_forge.application.runtime_context import get_runtime_value
from opennamu_forge.config.runtime_database import get_current_database_runtime_options
from opennamu_forge.infrastructure.setting_repository import OtherSettingRepository
from opennamu_forge.infrastructure.user_setting_repository import UserSettingRepository

orjson_module: Any | None = importlib.import_module("orjson") if importlib.util.find_spec("orjson") else None
re: Any = importlib.import_module("regex") if importlib.util.find_spec("regex") else stdlib_re


def json_dumps(obj: Any) -> str:
    if orjson_module is not None:
        return orjson_module.dumps(obj).decode("utf-8")
    return json.dumps(obj)


def json_loads(s: str | bytes) -> Any:
    if orjson_module is not None:
        return orjson_module.loads(s if isinstance(s, bytes) else s.encode("utf-8"))
    return json.loads(s)

def get_time():
    return str(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))

def db_change(data):
    set_data = get_runtime_value("db_type")
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

def ip_check(d_type=0):
    ip = "::1"
    if d_type == 0 and (flask.session and "id" in flask.session):
        ip = flask.session["id"]
    else:
        set_data = get_runtime_value("load_ip_select")
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

def get_main_skin_set(flask_session, set_name, ip):
    other_settings = OtherSettingRepository(get_current_database_runtime_options())
    user_settings = UserSettingRepository(get_current_database_runtime_options())

    if ip_or_user(ip) == 0:
        set_data = user_settings.get(ip, set_name) or "default"
    else:
        set_data = flask_session[set_name] if set_name in flask_session and flask_session[set_name] != "" else "default"

    if set_data == "default":
        set_data = other_settings.get(set_name) or "default"

    return set_data
