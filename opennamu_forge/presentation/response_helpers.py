from __future__ import annotations

import asyncio
import html
import os

import flask
import nest_asyncio

from opennamu_forge.presentation.dependencies import get_other_setting_repository
from opennamu_forge.presentation.encoding_helpers import json_loads
from opennamu_forge.presentation.gopennamu_gateway import python_to_golang
from opennamu_forge.presentation.shared.sql_dialect import re

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
