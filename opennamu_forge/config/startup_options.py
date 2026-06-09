from __future__ import annotations

from typing import Any


def get_init_set_list(need: str = "all") -> dict[str, Any]:
    init_set_list: dict[str, dict[str, Any]] = {
        "host": {
            "display": "Host",
            "require": "conv",
            "default": "0.0.0.0",
        },
        "port": {
            "display": "Port",
            "require": "conv",
            "default": "3000",
        },
        "golang_port": {
            "display": "Golang port",
            "require": "conv",
            "default": "3001",
        },
        "language": {
            "display": "Language",
            "require": "select",
            "default": "ko-KR",
            "list": ["ko-KR", "en-US"],
        },
        "markup": {
            "display": "Markup",
            "require": "select",
            "default": "namumark",
            "list": ["namumark", "namumark_beta", "macromark", "markdown", "custom", "raw"],
        },
        "encode": {
            "display": "Encryption method",
            "require": "select",
            "default": "sha3",
            "list": ["sha3", "sha3-salt", "sha3-512", "sha3-512-salt"],
        },
    }

    if need == "all":
        return init_set_list
    return init_set_list[need]
