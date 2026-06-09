from __future__ import annotations

import os

from opennamu_forge.presentation.gopennamu_gateway import python_to_golang
from opennamu_forge.presentation.response_helpers import get_lang


async def skin_check(set_n=0):
    res = await python_to_golang("api_func_skin_name", {"set_n": str(set_n)})
    raw = res["data"]

    norm = os.path.normpath(raw)
    parts = norm.split(os.sep)
    if "views" in parts:
        idx = parts.index("views")
        rel_parts = parts[idx + 1 :]
    else:
        rel_parts = parts

    return "/".join(rel_parts)


async def wiki_set():
    data = await python_to_golang("api_func_wiki_set", {})

    return data["data"]


async def wiki_custom():
    data = await python_to_golang("api_func_wiki_custom", {})

    return data["data"]


async def load_skin(data="", set_n=0, default=0):
    skin_return_data = []
    skin_return_data_str = ""

    skin_list_get = os.listdir("views")
    if default == 1:
        skin_list_get = ["default"] + skin_list_get

    for skin_data in skin_list_get:
        if skin_data != "default":
            see_data = skin_data
        else:
            see_data = await get_lang("default")

        if skin_data != "main_css":
            if set_n == 0:
                if skin_data == data:
                    skin_return_data_str = (
                        '<option value="' + skin_data + '">' + see_data + "</option>" + skin_return_data_str
                    )
                else:
                    skin_return_data_str += '<option value="' + skin_data + '">' + see_data + "</option>"
            else:
                if skin_data == data:
                    skin_return_data = [skin_data] + skin_return_data
                else:
                    skin_return_data += [skin_data]

    if set_n == 0:
        return skin_return_data_str

    return skin_return_data
