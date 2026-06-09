from .tool.func import *

async def user_alarm_delete(id = ''):
    with get_db_connect() as conn:
        user_notices = get_user_notice_repository()
        ip = ip_check()
    
        if id != '':
            user_notices.delete(ip, str(id))
        else:
            user_notices.delete_all(ip)

        return redirect(conn, '/alarm')
