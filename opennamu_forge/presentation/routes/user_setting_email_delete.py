from opennamu_forge.presentation.shared.func import (
    ip_check,
    ip_or_user,
)
from opennamu_forge.presentation.response_helpers import redirect
from opennamu_forge.presentation.dependencies import get_user_setting_repository
async def user_setting_email_delete():
    user_settings = get_user_setting_repository()

    ip = ip_check()
    if ip_or_user(ip) == 0:
        user_settings.delete(ip, "email")

    return redirect('/change')
