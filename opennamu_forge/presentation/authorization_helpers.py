from __future__ import annotations

from typing import Any, cast

from opennamu_forge.presentation.gopennamu_gateway import python_to_golang
from opennamu_forge.presentation.shared.sql_dialect import ip_check


async def level_check(ip: str = "") -> Any:
    ip = ip_check() if ip == "" else ip

    data = cast(dict[str, Any], await python_to_golang("api_func_level", {"ip": ip}))

    return data["data"]


async def acl_check(
    name: str = "",
    tool: str = "",
    topic_num: str = "",
    ip: str = "",
    memo: str = "",
) -> int:
    ip = ip_check() if ip == "" else ip

    data = cast(
        dict[str, Any],
        await python_to_golang(
            "api_func_acl",
            {
                "ip": ip,
                "name": name,
                "topic_number": topic_num,
                "tool": tool,
            },
        ),
    )

    result = 0 if data["data"] else 1

    if memo != "" and result == 0:
        await python_to_golang(
            "api_func_auth_post",
            {
                "ip": ip,
                "what": memo,
            },
        )

    return result


async def ban_check(ip: str | None = None, tool: str = "") -> list[Any]:
    ip = ip_check() if not ip else ip
    tool = "" if not tool else tool

    data = cast(
        dict[str, Any],
        await python_to_golang(
            "api_func_ban",
            {
                "ip": ip,
                "type": tool,
            },
        ),
    )
    ban = 1 if data["ban"] == "true" else 0

    return [ban, data["ban_type"]]
