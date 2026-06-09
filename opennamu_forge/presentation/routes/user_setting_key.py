from opennamu_forge.presentation.shared.func import (
    ip_check,
    ip_or_user,
)
from opennamu_forge.presentation.text_helpers import load_random_key
from opennamu_forge.presentation.response_helpers import redirect
from opennamu_forge.presentation.dependencies import get_user_setting_repository
async def user_setting_key():
    user_settings = get_user_setting_repository()

    ip = ip_check()
    if ip_or_user(ip) == 0:
        while 1:
            key = load_random_key()
            if not user_settings.data_exists("random_key", key):
                break

        user_settings.upsert(ip, "random_key", key)

    return redirect('/change')
