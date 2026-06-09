from __future__ import annotations

import html
import os

from PIL import Image

from opennamu_forge.presentation.encoding_helpers import sha224_replace, url_pas
from opennamu_forge.presentation.file_helpers import load_image_url
from opennamu_forge.presentation.response_helpers import get_lang
from opennamu_forge.presentation.shared.sql_dialect import get_main_skin_set, re


async def build_category_view(name, backlinks, session, ip):
    category_doc = ""
    category_sub = ""
    category_total = ""
    count_sub_category = 0
    count_category = 0

    category_sql = backlinks.list_distinct_links_by_title_type(name, "cat")
    for data in category_sql:
        link_view = data
        if get_main_skin_set(session, "main_css_category_change_title", ip) != "off":
            db_data = backlinks.get_data(name, data, "cat_view")
            if db_data != "":
                link_view = db_data

        link_blur = ""
        if backlinks.exists(name, data, "cat_blur"):
            link_blur = "opennamu_forge_category_blur"

        if data.startswith("category:"):
            category_sub += '<li><a class="' + link_blur + '" href="/w/' + url_pas(data) + '">' + html.escape(link_view) + "</a></li>"
            count_sub_category += 1
        else:
            category_doc += (
                '<li><a class="'
                + link_blur
                + '" href="/w/'
                + url_pas(data)
                + '">'
                + html.escape(link_view)
                + '</a> <a class="opennamu_forge_link_inter" href="/xref/'
                + url_pas(data)
                + '">('
                + await get_lang("backlink")
                + ")</a></li>"
            )
            count_category += 1

    if category_sub != "":
        category_total += (
            '<h2 id="cate_under">'
            + await get_lang("under_category")
            + "</h2><ul><li>"
            + await get_lang("all")
            + " : "
            + str(count_sub_category)
            + "</li>"
            + category_sub
            + "</ul>"
        )

    if category_doc != "":
        category_total += (
            '<h2 id="cate_normal">'
            + await get_lang("category_title")
            + "</h2><ul><li>"
            + await get_lang("all")
            + " : "
            + str(count_category)
            + "</li>"
            + category_doc
            + "</ul>"
        )

    return category_total


async def build_file_view(name, rev):
    mime_type = re.search(r"([^.]+)$", name)
    if mime_type:
        mime_type = mime_type.group(1)
    else:
        mime_type = "jpg"

    file_name = re.sub(r"\.([^.]+)$", "", name)
    file_name = re.sub(r"^file:", "", file_name)
    file_all_name = sha224_replace(file_name) + "." + mime_type
    file_path_name = os.path.join(load_image_url(), file_all_name)
    if not os.path.exists(file_path_name):
        return "", []

    try:
        img = Image.open(file_path_name)
        width, height = img.size
        file_res = str(width) + "x" + str(height)
    except Exception:
        file_res = "Vector"

    file_size = str(round(os.path.getsize(file_path_name) / 1000, 1))
    file_data = '''
        <img src="/image/''' + url_pas(file_all_name) + '''.cache_v''' + rev + '''">
        <h2>''' + await get_lang("data") + '''</h2>
        <table>
            <tr><td>''' + await get_lang("url") + '''</td><td><a href="/image/''' + url_pas(file_all_name) + '''">''' + await get_lang("link") + '''</a></td></tr>
            <tr><td>''' + await get_lang("volume") + '''</td><td>''' + file_size + '''KB</td></tr>
            <tr><td>''' + await get_lang("resolution") + '''</td><td>''' + file_res + '''</td></tr>
        </table>
        <h2>''' + await get_lang("content") + '''</h2>
    '''

    return file_data, [["delete_file/" + url_pas(name), await get_lang("file_delete")]]


def build_redirect_notice(last_page, name, redirect_text_raw, end_data):
    redirect_text = redirect_text_raw if redirect_text_raw != "" else "{0} ➤ {1}"
    try:
        redirect_text = redirect_text.format(
            '<a href="/w_from/' + url_pas(last_page) + '">' + html.escape(last_page) + "</a>",
            "<b>" + html.escape(name) + "</b>",
        )
    except Exception:
        redirect_text = "{0} ➤ {1}"
        redirect_text = redirect_text.format(
            '<a href="/w_from/' + url_pas(last_page) + '">' + html.escape(last_page) + "</a>",
            "<b>" + html.escape(name) + "</b>",
        )

    return '''
        <div class="opennamu_forge_redirect" id="redirect">
            ''' + redirect_text + '''
        </div>
        <hr class="main_hr">
    ''' + end_data


async def build_trace_view(recent_documents, end_data):
    return (
        '<div class="opennamu_forge_trace">'
        + '<a class="opennamu_forge_trace_button" href="javascript:opennamu_forge_do_trace_spread();"> (+)</a>'
        + await get_lang("trace")
        + " : "
        + " ← ".join(
            [
                '<a href="/w/' + url_pas(for_a) + '">' + html.escape(for_a) + "</a>"
                for for_a in reversed(recent_documents)
            ]
        )
        + "</div>"
        + '<hr class="main_hr">'
        + end_data
    )
