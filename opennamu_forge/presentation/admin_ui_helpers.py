from __future__ import annotations

from opennamu_forge.presentation.gopennamu_gateway import python_to_golang


def get_default_admin_group():
    return ["owner", "user", "ip", "ban"]


async def get_acl_list(type_data="normal"):
    if type_data == "user":
        type_data = "user_document"

    data = await python_to_golang("api_list_acl", {"type": type_data})

    return data["data"]
