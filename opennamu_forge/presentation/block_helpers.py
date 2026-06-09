from __future__ import annotations

from opennamu_forge.presentation.dependencies import get_recent_block_repository
from opennamu_forge.presentation.shared.sql_dialect import get_time


def ban_insert(name, end, why, login, blocker, type_d=None, release=0):
    now_time = get_time()
    band = type_d if type_d else ""
    recent_blocks = get_recent_block_repository()

    recent_blocks.close_ongoing(name, band)
    if release == 1:
        recent_blocks.add_record(
            name,
            "release",
            now_time,
            blocker,
            why,
            band,
            "",
            "",
        )
    else:
        login = login if login != "" else ""
        r_time = end if end != "0" else ""

        recent_blocks.add_record(
            name,
            r_time,
            now_time,
            blocker,
            why,
            band,
            "1",
            login,
        )
