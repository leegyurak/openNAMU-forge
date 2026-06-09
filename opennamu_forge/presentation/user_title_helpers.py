from __future__ import annotations

from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.dependencies import get_user_setting_repository
from opennamu_forge.presentation.response_helpers import get_lang
from opennamu_forge.presentation.shared.sql_dialect import ip_check


async def get_user_title_list(ip=""):
    ip = ip_check() if ip == "" else ip

    user_title = {
        "": await get_lang("default"),
        "🌳": "🌳 newbie",
    }

    user_settings = get_user_setting_repository()

    if user_settings.exists(ip, "get_🥚"):
        user_title["🥚"] = "🥚 easter_egg"

    if user_settings.exists(ip, "challenge_first_contribute"):
        user_title["🔰"] = "🔰 first_contribute"

    if user_settings.exists(ip, "challenge_tenth_contribute"):
        user_title["📝"] = "📝 tenth_contribute"

    if user_settings.exists(ip, "challenge_hundredth_contribute"):
        user_title["🖊️"] = "🖊️ hundredth_contribute"

    if user_settings.exists(ip, "challenge_thousandth_contribute"):
        user_title["🏅"] = "🏅 thousandth_contribute"

    if user_settings.exists(ip, "challenge_first_discussion"):
        user_title["💬"] = "💬 first_discussion"

    if user_settings.exists(ip, "challenge_tenth_discussion"):
        user_title["💡"] = "💡 tenth_discussion"

    if user_settings.exists(ip, "challenge_hundredth_discussion"):
        user_title["📢"] = "📢 hundredth_discussion"

    if user_settings.exists(ip, "challenge_thousandth_discussion"):
        user_title["📜"] = "📜 thousandth_discussion"

    if user_settings.exists(ip, "challenge_admin"):
        user_title["☑️"] = "☑️ before_admin"

    if await acl_check(tool="all_admin_auth") != 1:
        user_title["✅"] = "✅ admin"

    return user_title
