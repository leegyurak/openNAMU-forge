from opennamu_forge.presentation.shared.func import ip_check
from opennamu_forge.presentation.response_helpers import redirect
from opennamu_forge.presentation.dependencies import get_user_notice_repository
async def user_alarm_delete(id = ''):
    user_notices = get_user_notice_repository()
    ip = ip_check()

    if id != '':
        user_notices.delete(ip, str(id))
    else:
        user_notices.delete_all(ip)

    return redirect('/alarm')
