from __future__ import annotations

import random


def load_random_key(long: int = 128) -> str:
    return "".join(random.choice("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(long))

def leng_check(old_length: int, new_length: int) -> str:
    return "0" if old_length == new_length else (("-" + str(old_length - new_length)) if old_length > new_length else ("+" + str(new_length - old_length)))

def number_check(data, f=0):
    try:
        float(data) if f == 1 else int(data)
        return data
    except Exception:
        return "1"

def get_tool_js_safe(data: str) -> str:
    data = data.replace("\n", "\\\\n")
    data = data.replace("\\", "\\\\")
    data = data.replace("'", "\\'")
    data = data.replace('"', '\\"')

    return data

def cache_v() -> str:
    return ".cache_v289"

def cut_100(data):
    return ""
