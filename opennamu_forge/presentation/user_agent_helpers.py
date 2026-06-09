from __future__ import annotations

from opennamu_forge.presentation.dependencies import get_other_setting_repository, get_user_agent_repository


def ua_plus(u_id, u_ip, u_agent, time):
    rep_data = get_other_setting_repository().get("ua_get")
    if rep_data == "":
        get_user_agent_repository().add(u_id, u_ip, u_agent, time)
