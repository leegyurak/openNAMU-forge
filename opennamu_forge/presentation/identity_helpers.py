from __future__ import annotations

from typing import Any, cast

from opennamu_forge.presentation.gopennamu_gateway import python_to_golang


async def ip_pas(raw_ip: str | list[str]) -> str | dict[str, str]:
    other_set: dict[str, str] = {}
    return_single = not isinstance(raw_ip, list)
    get_ip = [raw_ip] if return_single else raw_ip

    for index, ip in enumerate(get_ip, start=1):
        other_set["data_" + str(index)] = ip

    data = cast(dict[str, Any], await python_to_golang("api_func_ip_post", other_set))
    result = cast(dict[str, str], data["data"])
    return result[raw_ip] if return_single else result
