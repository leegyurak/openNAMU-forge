from __future__ import annotations

import datetime

import flask

from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.block_helpers import ban_insert
from opennamu_forge.presentation.dependencies import (
    get_history_repository,
    get_html_filter_repository,
    get_other_setting_repository,
    get_topic_repository,
    get_user_setting_repository,
)
from opennamu_forge.presentation.shared.sql_dialect import ip_check, re
from opennamu_forge.presentation.text_helpers import number_check


def get_edit_text_bottom(tool=""):
    settings = get_other_setting_repository()
    b_text = ""

    db_data = settings.get("edit_bottom_text")
    if db_data != "":
        b_text = db_data + '<hr class="main_hr">'

    if tool != "":
        if tool == "edit":
            db_data = settings.get("edit_only_bottom_text")
        elif tool == "move":
            db_data = settings.get("move_bottom_text")
        elif tool == "delete":
            db_data = settings.get("delete_bottom_text")
        else:
            db_data = settings.get("revert_bottom_text")

        if db_data != "":
            b_text = db_data + '<hr class="main_hr">'

    return b_text


def get_edit_text_bottom_check_box():
    cccb_text = ""

    sql_d = get_other_setting_repository().get("copyright_checkbox_text")
    if sql_d != "":
        checked = ""
        if flask.session and "bottom_check_box_pass" in flask.session:
            checked = "checked"

        cccb_text = (
            '<label class="__ON_CHECKLABEL__"><input class="__ON_CHECKBOX__" type="checkbox" '
            'name="copyright_agreement" value="yes" '
            + checked
            + "> "
            + sql_d
            + "</label>"
            + '<hr class="main_hr">'
        )

    return cccb_text


def do_edit_text_bottom_check_box_check(data):
    db_data = get_other_setting_repository().get("copyright_checkbox_text")
    if db_data != "":
        if "bottom_check_box_pass" in flask.session and flask.session["bottom_check_box_pass"] > 0:
            pass
        elif data != "yes":
            return 1

    if "bottom_check_box_pass" not in flask.session:
        flask.session["bottom_check_box_pass"] = 1

    return 0


async def do_edit_send_check(data):
    db_data = get_other_setting_repository().get("edit_bottom_compulsion")
    if db_data != "" and await acl_check("", "edit_bottom_compulsion") == 1 and data == "":
        return 1

    return 0


async def do_edit_slow_check(do_type="edit"):
    settings = get_other_setting_repository()

    if do_type == "edit":
        slow_edit = settings.get("slow_edit")
    else:
        slow_edit = settings.get("slow_thread")

    if slow_edit != "" and await acl_check("", "slow_edit") == 1:
        slow_edit = int(number_check(slow_edit))

        if do_type == "edit":
            last_edit_data = get_history_repository().latest_date_by_ip(ip_check())
        else:
            last_edit_data = get_topic_repository().latest_date_by_ip(ip_check())

        if last_edit_data:
            last_edit_data = int(re.sub(" |:|-", "", last_edit_data))
            now_edit_data = int(
                (datetime.datetime.now() - datetime.timedelta(seconds=slow_edit)).strftime("%Y%m%d%H%M%S")
            )

            if last_edit_data > now_edit_data:
                return 1

    return 0


async def do_edit_filter(data):
    ip = ip_check()
    if await acl_check(tool="edit_filter_pass") == 1:
        for data_list in get_html_filter_repository().list_regex_filters_with_plus():
            match = re.compile(data_list.plus, re.I)
            if match.search(data):
                end = "0" if data_list.plus_t == "X" else data_list.plus_t

                if end != "0":
                    end = int(number_check(end))
                    time = datetime.datetime.now()
                    plus = datetime.timedelta(seconds=end)
                    r_time = (time + plus).strftime("%Y-%m-%d %H:%M:%S")
                else:
                    r_time = "0"

                get_user_setting_repository().upsert(ip, "edit_filter", data)

                ban_insert(
                    ip,
                    r_time,
                    "edit filter",
                    "",
                    "tool:edit filter",
                )

                return 1

    return 0


def do_title_length_check(name, check_type="document"):
    settings = get_other_setting_repository()

    if check_type == "topic":
        db_data = settings.get("title_topic_max_length")
        if db_data != "":
            db_data = int(number_check(db_data))
            if len(name) > db_data:
                return 1
    else:
        db_data = settings.get("title_max_length")
        if db_data != "":
            db_data = int(number_check(db_data))
            if len(name) > db_data:
                return 1

    return 0
