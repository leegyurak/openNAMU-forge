from .tool.func import *

async def user_setting_email_delete():
    with get_db_connect() as conn:
        user_settings = get_user_setting_repository()

        ip = ip_check()
        if ip_or_user(ip) == 0:
            user_settings.delete(ip, "email")
    
        return redirect(conn, '/change')
