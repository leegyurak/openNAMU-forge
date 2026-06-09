from __future__ import annotations

import html

from opennamu_forge.presentation.dependencies import get_html_filter_repository, get_other_setting_repository
from opennamu_forge.presentation.response_helpers import get_lang
from opennamu_forge.presentation.shared.sql_dialect import ip_or_user
from opennamu_forge.presentation.text_helpers import get_tool_js_safe


async def edit_button():
    insert_list = []

    db_data = get_html_filter_repository().list_by_kind("edit_top")
    for get_data in db_data:
        insert_list += [[get_data.plus, get_data.html]]

    data = ""
    for insert_data in insert_list:
        data += (
            "<a href=\"javascript:do_insert_data('"
            + get_tool_js_safe(insert_data[0])
            + "');\">("
            + html.escape(insert_data[1])
            + ")</a> "
        )

    data += (" " if data != "" else "") + '<a href="/filter/edit_top">(' + await get_lang("add") + ")</a>"
    data += '<hr class="main_hr">'

    return data


async def ip_warning():
    if ip_or_user() != 0:
        data = get_other_setting_repository().get("no_login_warning")
        if data != "":
            text_data = '<span>' + data + '</span><hr class="main_hr">'
        else:
            text_data = '<span>' + await get_lang("no_login_warning") + '</span><hr class="main_hr">'
    else:
        text_data = ""

    return text_data
