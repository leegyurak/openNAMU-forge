import os

from opennamu_forge.application.version import VERSION_INFO
from opennamu_forge.infrastructure.logging import get_logger
from opennamu_forge.presentation.dependencies import (
    get_discussion_service,
    get_history_mutation_service,
    get_user_registration_service,
)

__all__ = [
    "add_alarm",
    "add_user",
    "do_add_thread",
    "do_reload_recent_thread",
    "get_db_table_list",
    "history_plus",
    "history_plus_rc_max",
    "opennamu_forge_make_list",
]

logger = get_logger(__name__)
version_list = VERSION_INFO

logger.info("Version : %s", version_list["r_ver"])
logger.info("DB set version : %s", version_list["c_ver"])
logger.info("Skin set version : %s", version_list["s_ver"])

os.makedirs("data", exist_ok=True)
logger.info('uv-managed dependencies are expected. Run "uv sync --extra performance --extra dev" before startup.')


async def opennamu_forge_make_list(left="", right="", bottom="", class_name=""):
    data_html = f'<span class="{class_name}">'
    data_html += '<div class="opennamu_forge_recent_change">'
    data_html += left
    data_html += '<div style="float: right;">'
    data_html += right
    data_html += "</div>"
    data_html += '<div style="clear: both;"></div>'

    if bottom != "":
        data_html += "<hr>"
        data_html += bottom

    data_html += "</div>"
    data_html += '<hr class="main_hr">'
    data_html += "</span>"

    return data_html


def get_db_table_list():
    return {
        "data_set": ["doc_name", "doc_rev", "set_name", "set_data"],
        "data": ["title", "data", "type"],
        "history": ["id", "title", "data", "date", "ip", "send", "leng", "hide", "type"],
        "rc": ["id", "title", "date", "type"],
        "acl": ["title", "data", "type"],
        "back": ["title", "link", "type", "data"],
        "topic_set": ["thread_code", "set_name", "set_id", "set_data"],
        "rd": ["title", "sub", "code", "date", "band", "stop", "agree", "acl"],
        "topic": ["id", "data", "date", "ip", "block", "top", "code"],
        "rb": ["block", "end", "today", "blocker", "why", "band", "login", "ongoing"],
        "other": ["name", "data", "coverage"],
        "html_filter": ["html", "kind", "plus", "plus_t"],
        "vote": ["name", "id", "subject", "data", "user", "type", "acl"],
        "alist": ["name", "acl"],
        "re_admin": ["who", "what", "time"],
        "ua_d": ["name", "ip", "ua", "today", "sub"],
        "user_set": ["name", "id", "data"],
        "user_notice": ["id", "name", "data", "date", "readme"],
        "bbs_set": ["set_name", "set_code", "set_id", "set_data"],
        "bbs_data": ["set_name", "set_code", "set_id", "set_data"],
    }


def do_add_thread(thread_code, thread_data, thread_top="", thread_id=""):
    get_discussion_service().add_thread_comment(
        thread_code,
        thread_data,
        thread_top,
        thread_id,
    )


def do_reload_recent_thread(topic_num, date, name="", sub=""):
    get_discussion_service().reload_recent_thread(topic_num, date, name, sub)


async def add_alarm(to_user, from_user, context):
    await get_discussion_service().add_alarm(to_user, from_user, context)


def add_user(user_name, user_pw, user_email="", user_encode=""):
    get_user_registration_service().add_user(user_name, user_pw, user_email, user_encode)


def history_plus_rc_max(mode):
    get_history_mutation_service().enforce_recent_change_limit(mode)


def history_plus(title, data, date, ip, send, leng, t_check="", mode=""):
    return get_history_mutation_service().add_history(title, data, date, ip, send, leng, t_check, mode)
