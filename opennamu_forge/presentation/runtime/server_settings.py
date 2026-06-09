from __future__ import annotations

import os
from collections.abc import Callable, Mapping
from typing import cast

from opennamu_forge.application.runtime_context import set_runtime_value
from opennamu_forge.config.startup_options import get_init_set_list
from opennamu_forge.infrastructure.logging import get_logger

logger = get_logger(__name__)

def resolve_server_settings(
    settings,
    *,
    env_get: Callable[[str], str | None] = os.getenv,
    input_func: Callable[[str], str] = input,
) -> dict[str, str]:
    server_set: dict[str, str] = {}
    server_set_var = get_init_set_list()
    server_set_env = {
        "host": env_get("NAMU_HOST"),
        "golang_port": env_get("NAMU_GOLANGPORT"),
        "port": env_get("NAMU_PORT"),
        "language": env_get("NAMU_LANG"),
        "markup": env_get("NAMU_MARKUP"),
        "encode": env_get("NAMU_ENCRYPT"),
    }

    for key in server_set_var:
        server_set_val = _resolve_server_setting_value(
            key,
            server_set_var[key],
            settings.get(key),
            server_set_env[key],
            input_func,
        )

        if settings.get(key) == "":
            settings.upsert(key, server_set_val)

        logger.info("%s : %s", server_set_var[key]["display"], server_set_val)
        server_set[key] = server_set_val

    _apply_runtime_values(server_set)

    return server_set

def _resolve_server_setting_value(
    key: str,
    option: Mapping[str, object],
    stored_value: str,
    env_value: str | None,
    input_func: Callable[[str], str],
) -> str:
    if stored_value != "":
        return stored_value

    if env_value is not None:
        return env_value

    server_set_val = input_func(_build_prompt(option))
    if server_set_val == "":
        return str(option["default"])

    option_list = cast(list[str], option["list"]) if "list" in option else []
    if option["require"] == "select" and server_set_val not in option_list:
        return str(option["default"])

    return server_set_val

def _build_prompt(option: Mapping[str, object]) -> str:
    if "list" in option:
        option_list = cast(list[str], option["list"])
        return (
            str(option["display"])
            + " ("
            + str(option["default"])
            + ") ["
            + ", ".join(option_list)
            + "] : "
        )

    return str(option["display"]) + " (" + str(option["default"]) + ") : "

def _apply_runtime_values(server_set: Mapping[str, str]) -> None:
    for key, value in server_set.items():
        set_runtime_value("setup_" + key, value)
