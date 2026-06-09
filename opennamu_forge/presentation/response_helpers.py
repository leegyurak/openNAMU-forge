from __future__ import annotations

import asyncio
import html
import os

import flask
import nest_asyncio

from opennamu_forge.presentation.authorization_helpers import ban_check
from opennamu_forge.presentation.dependencies import get_other_setting_repository
from opennamu_forge.presentation.encoding_helpers import json_loads
from opennamu_forge.presentation.gopennamu_gateway import python_to_golang
from opennamu_forge.presentation.shared.sql_dialect import ip_check, re
from opennamu_forge.presentation.text_helpers import number_check

global_lang_data: dict[str, str] = {}

async def render_template(name, data, sub, menu, other=None, option=None):
    other_items = [] if other is None else other
    option_items = {} if option is None else option
    other_set = {
        "name": name,
        "data": data,
        "sub": [sub] + other_items,
        "menu": menu,
        "option": {
            "path": flask.request.path,
        },
    }

    other_set["option"].update(option_items)

    return await python_to_golang("post", other_set=other_set, path="template")

async def http_warning():
    return (
        '<div id="opennamu_forge_http_warning_text"></div>'
        '<span style="display: none;" id="opennamu_forge_http_warning_text_lang">'
        + await get_lang("http_warning")
        + "</span>"
    )

def load_domain(data_type="normal"):
    try:
        sys_host = flask.request.host
    except Exception:
        sys_host = ""

    if data_type == "full":
        settings = get_other_setting_repository()
        return (settings.get("http_select") or "http") + "://" + (settings.get("domain") or sys_host)

    return get_other_setting_repository().get("domain") or sys_host

def redirect(data="/"):
    return flask.redirect(load_domain("full") + data)

async def get_lang(data, safe=0):
    if data in global_lang_data:
        if safe == 1:
            return html.unescape(global_lang_data[data])
        return global_lang_data[data]

    lang = json_loads(open(os.path.join("lang", "en-US.json"), encoding="utf-8").read())

    other_set = {
        "data": " ".join([title for title in lang if title[0] != "_"]),
        "safe": "",
    }

    res = await python_to_golang("api_func_language", other_set)
    if res["response"] == "ok":
        for load_data in res["data"]:
            global_lang_data[load_data] = res["data"][load_data]

    if data in global_lang_data:
        if safe == 1:
            return html.unescape(global_lang_data[data])
        return global_lang_data[data]
    return data + " (M)"

def load_lang(data, safe=0):
    try:
        loop = asyncio.get_running_loop()
        if loop.is_running():
            nest_asyncio.apply()
            return loop.run_until_complete(get_lang(data, safe))
    except RuntimeError:
        return asyncio.run(get_lang(data, safe))

    return asyncio.run(get_lang(data, safe))

async def render_simple_set(data):
    toc_data = ""
    toc_regex = r"<h([1-6])>([^<>]+)<\/h[1-6]>"
    toc_search_data = re.findall(toc_regex, data)
    heading_stack = [0, 0, 0, 0, 0, 0]

    if toc_search_data:
        toc_data += (
            '<div class="opennamu_forge_TOC" id="toc">'
            '<span class="opennamu_forge_TOC_title">'
            + await get_lang("toc")
            + "</span><br>"
        )

    for toc_search_in in toc_search_data:
        heading_level = int(toc_search_in[0])
        heading_stack[heading_level - 1] += 1
        for for_a in range(heading_level, 6):
            heading_stack[for_a] = 0

        heading_stack_str = "".join([str(for_a) + "." if for_a != 0 else "" for for_a in heading_stack])
        heading_stack_str = re.sub(r"\.$", "", heading_stack_str)

        toc_data += (
            '<br><span class="opennamu_forge_TOC_list">'
            + ('<span style="margin-left: 10px;"></span>' * heading_stack_str.count("."))
            + '<a href="#s-'
            + heading_stack_str
            + '">'
            + heading_stack_str
            + ".</a>"
            + toc_search_in[1]
            + "</span>"
        )

        data = re.sub(
            toc_regex,
            '<h'
            + toc_search_in[0]
            + ' id="s-'
            + heading_stack_str
            + '"><a href="#toc">'
            + heading_stack_str
            + ".</a> "
            + toc_search_in[1]
            + "</h"
            + toc_search_in[0]
            + ">",
            data,
            count=1,
        )

    if toc_data != "":
        toc_data += "</div>"

    footnote_data = ""
    footnote_regex = r"<sup>((?:(?!<sup>|<\/sup>).)+)<\/sup>"
    footnote_search_data = re.findall(footnote_regex, data)
    footnote_count = 1
    if footnote_search_data:
        footnote_data += '<div class="opennamu_forge_footnote">'

    for footnote_search in footnote_search_data:
        footnote_count_str = str(footnote_count)

        if footnote_count != 1:
            footnote_data += "<br>"

        footnote_data += (
            '<a id="fn-'
            + footnote_count_str
            + '" href="#rfn-'
            + footnote_count_str
            + '">('
            + footnote_count_str
            + ")</a> "
            + footnote_search
        )
        data = re.sub(
            footnote_regex,
            '<sup id="rfn-'
            + footnote_count_str
            + '"><a href="#fn-'
            + footnote_count_str
            + '">('
            + footnote_count_str
            + ")</a></sup>",
            data,
            count=1,
        )

        footnote_count += 1

    if footnote_data != "":
        footnote_data += "</div>"

    return toc_data + data + footnote_data


async def re_error(data):
    if data == 0:
        if (await ban_check())[0] == 1:
            end = '<div id="opennamu_forge_get_user_info">' + html.escape(ip_check()) + "</div>"
        else:
            end = "<ul><li>" + await get_lang("authority_error") + "</li></ul>"

        return await render_template(
            await get_lang("error"),
            "<h2>" + await get_lang("error") + "</h2>" + end,
            0,
            0,
        ), 401

    title = await get_lang("error")
    sub_title = title
    return_code = 400

    num = data
    if num == 1:
        data = await get_lang("no_login_error")
    elif num == 2:
        data = await get_lang("no_exist_user_error")
    elif num == 3:
        data = await get_lang("authority_error")
    elif num == 4:
        data = await get_lang("no_admin_block_error")
    elif num == 5:
        data = await get_lang("error_skin_set")
    elif num == 8:
        data = (
            await get_lang("long_id_error")
            + "<br>"
            + await get_lang("id_char_error")
            + ' <a href="/filter/name_filter">('
            + await get_lang("id_filter_list")
            + ")</a><br>"
            + await get_lang("same_id_exist_error")
        )
    elif num == 9:
        data = await get_lang("file_exist_error")
    elif num == 10:
        data = await get_lang("password_error")
    elif num == 11:
        data = await get_lang("topic_long_error")
    elif num == 12:
        data = await get_lang("email_error")
    elif num == 13:
        data = await get_lang("recaptcha_error")
    elif num == 14:
        data = (
            await get_lang("file_extension_error")
            + ' <a href="/filter/extension_filter">('
            + await get_lang("extension_filter_list")
            + ")</a>"
        )
    elif num == 15:
        data = await get_lang("edit_record_error")
    elif num == 16:
        data = await get_lang("same_file_error")
    elif num == 17:
        db_data = get_other_setting_repository().get("upload")
        file_max = number_check(db_data) if db_data != "" else "2"
        data = await get_lang("file_capacity_error") + file_max
    elif num == 18:
        data = await get_lang("email_send_error")
    elif num == 19:
        data = await get_lang("move_error")
    elif num == 20:
        data = await get_lang("password_diffrent_error")
    elif num == 21:
        data = await get_lang("edit_filter_error")
    elif num == 22:
        data = await get_lang("file_name_error")
    elif num == 23:
        data = await get_lang("regex_error")
    elif num == 24:
        db_data = get_other_setting_repository().get("slow_edit")
        data = await get_lang("fast_edit_error") + db_data
    elif num == 25:
        data = await get_lang("too_many_dec_error")
    elif num == 26:
        data = await get_lang("application_not_found")
    elif num == 27:
        data = await get_lang("invalid_password_error")
    elif num == 28:
        data = await get_lang("watchlist_overflow_error")
    elif num == 29:
        data = await get_lang("copyright_disagreed")
    elif num == 30:
        data = await get_lang("ie_wrong_callback")
    elif num == 33:
        data = await get_lang("restart_fail_error")
    elif num == 35:
        data = await get_lang("same_email_error")
    elif num == 36:
        data = await get_lang("input_email_error")
    elif num == 37:
        data = await get_lang("error_edit_send_request")
    elif num == 38:
        db_data = get_other_setting_repository().get("title_max_length")
        data = await get_lang("error_title_length_too_long") + db_data
    elif num == 39:
        db_data = get_other_setting_repository().get("title_topic_max_length")
        data = await get_lang("error_title_length_too_long") + db_data
    elif num == 40:
        password_min_length = get_other_setting_repository().get("password_min_length")
        data = await get_lang("error_password_length_too_short") + password_min_length
    elif num == 41:
        db_data = get_other_setting_repository().get("edit_timeout")
        data = await get_lang("timeout_error") + db_data
    elif num == 42:
        db_data = get_other_setting_repository().get("slow_thread")
        data = await get_lang("fast_edit_error") + db_data
    elif num == 43:
        title = await get_lang("application_submitted")
        sub_title = title
        data = await get_lang("waiting_for_approval")
    elif num == 44:
        db_data = get_other_setting_repository().get("document_content_max_length")
        data = await get_lang("error_content_length_too_long") + db_data
    elif num == 45:
        data = await get_lang("cidr_error")
    elif num == 46:
        data = await get_lang("func_404_error")
        title = "404"
        return_code = 404
    elif num == 47:
        data = await get_lang("still_use_auth_error")
    elif num == 48:
        data = await get_lang("xss_data_include_error")
    elif num == 49:
        data = await get_lang("password_same_as_id_error")
    else:
        data = "???"

    if num == 5:
        if flask.request.path != "/skin_set":
            data += "<br>" + await get_lang("error_skin_set_old") + ' <a href="/skin_set">(' + await get_lang("go") + ")</a>"

        return await render_template(
            await get_lang("skin_set"),
            '<div id="main_skin_set">'
            + "<h2>"
            + await get_lang("error")
            + "</h2>"
            + "<ul>"
            + "<li>"
            + data
            + "</a></li>"
            + "</ul>"
            + "</div>",
            0,
            [["change", await get_lang("user_setting")], ["change/skin_set/main", await get_lang("main_skin_set")]],
        )

    return await render_template(
        title,
        "<h2>" + sub_title + "</h2>" + "<ul>" + "<li>" + data + "</li>" + "</ul>",
        0,
        0,
    ), return_code
