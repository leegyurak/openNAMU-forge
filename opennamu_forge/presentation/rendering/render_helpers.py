from __future__ import annotations

import flask

from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.dependencies import get_other_setting_repository
from opennamu_forge.presentation.rendering.renderer import class_do_render
from opennamu_forge.presentation.response_helpers import get_lang
from opennamu_forge.presentation.shared.sql_dialect import get_main_skin_set, ip_check
from opennamu_forge.presentation.text_helpers import number_check


async def render_set(doc_name="", doc_data="", data_type="view", markup="", parameter=None):
    parameter = {} if parameter is None else parameter

    return_type = True
    if data_type in ["api_from", "api_view", "api_thread", "api_include"]:
        return_type = False

    if await acl_check(doc_name, "render") == 1:
        if not return_type:
            return ["", ""]

        return ""

    if data_type == "":
        data_type = "view"
    elif data_type == "api_view":
        data_type = "view"
    elif data_type == "api_from":
        data_type = "from"
    elif data_type == "api_thread":
        data_type = "thread"
    elif data_type == "api_include":
        data_type = "include"

    doc_data = "" if doc_data is None else doc_data

    ip = ip_check()
    render_lang_data = {
        "toc": await get_lang("toc"),
        "category": await get_lang("category"),
    }

    db_data = get_other_setting_repository().get("category_text")
    if db_data != "":
        render_lang_data["category"] = db_data

    get_class_render = await class_do_render(render_lang_data, markup, parameter, render_set).do_render(
        doc_name,
        doc_data,
        data_type,
    )
    if data_type == "backlink":
        return ""

    get_class_render[0] = '<div class="opennamu_forge_render_complete">' + get_class_render[0] + "</div>"

    font_size_set_data = get_main_skin_set(flask.session, "main_css_font_size", ip)
    if font_size_set_data != "default":
        font_size_set_data = number_check(font_size_set_data)

        get_class_render[0] = (
            """<style>
                .opennamu_forge_render_complete {
                    font-size: """
            + font_size_set_data
            + """px !important;
                }
            </style>"""
            + get_class_render[0]
        )

    db_data = get_other_setting_repository().get("namumark_compatible")
    if db_data != "":
        get_class_render[0] = (
            """<style>
                .opennamu_forge_render_complete {
                    font-size: 15px !important;
                    line-height: 1.5;
                }

                .opennamu_forge_render_complete td {
                    padding: 5px 10px !important;
                    word-break: break-all;
                }

                .opennamu_forge_render_complete summary {
                    list-style: none !important;
                    font-weight: bold !important;
                }

                .opennamu_forge_render_complete .opennamu_forge_folding {
                    margin-bottom: 5px;
                }

                .opennamu_forge_render_complete .opennamu_forge_footnote {
                    padding-bottom: 30px;
                }

                .opennamu_forge_render_complete iframe {
                    display: block;
                }
            </style>"""
            + get_class_render[0]
        )

    table_set_data = get_main_skin_set(flask.session, "main_css_table_scroll", ip)
    if table_set_data == "on":
        get_class_render[0] = '<style>.table_safe { overflow-x: scroll; white-space: nowrap; }</style>' + get_class_render[0]

    joke_set_data = get_main_skin_set(flask.session, "main_css_view_joke", ip)
    if joke_set_data == "off":
        get_class_render[0] = '<style>.opennamu_forge_joke { display: none; }</style>' + get_class_render[0]

    math_set_data = get_main_skin_set(flask.session, "main_css_math_scroll", ip)
    if math_set_data == "on":
        get_class_render[0] = "<style>.katex .base { overflow-x: scroll; }</style>" + get_class_render[0]

    transparent_set_data = get_main_skin_set(flask.session, "main_css_table_transparent", ip)
    if transparent_set_data == "on":
        get_class_render[0] = (
            """<style>
                .table_safe td {
                    background: transparent !important;
                    color: inherit !important;
                }
            </style>"""
            + get_class_render[0]
        )

    if not return_type:
        return [get_class_render[0], get_class_render[1]]

    return (
        get_class_render[0]
        + '<script>window.addEventListener("DOMContentLoaded", function() {'
        + get_class_render[1]
        + "});</script>"
    )
