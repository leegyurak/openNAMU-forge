from __future__ import annotations

from opennamu_forge.presentation.response_helpers import get_lang


async def get_next_page_bottom(link, num, page, end=50):
    list_data = ""

    if num == 1:
        if len(page) == end:
            list_data += (
                '<hr class="main_hr">'
                + '<a href="'
                + link.format(str(num + 1))
                + '">('
                + await get_lang("next")
                + ")</a>"
            )
    elif len(page) != end:
        list_data += (
            '<hr class="main_hr">'
            + '<a href="'
            + link.format(str(num - 1))
            + '">('
            + await get_lang("previous")
            + ")</a>"
        )
    else:
        list_data += (
            '<hr class="main_hr">'
            + '<a href="'
            + link.format(str(num - 1))
            + '">('
            + await get_lang("previous")
            + ')</a> '
            + '<a href="'
            + link.format(str(num + 1))
            + '">('
            + await get_lang("next")
            + ")</a>"
        )

    return list_data
