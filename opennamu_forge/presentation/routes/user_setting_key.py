from .tool.func import *

async def user_setting_key():
    with get_db_connect() as conn:
        user_settings = get_user_setting_repository()

        ip = ip_check()
        if ip_or_user(ip) == 0:
            while 1:
                key = load_random_key()
                if not user_settings.data_exists("random_key", key):
                    break

            user_settings.upsert(ip, "random_key", key)

        return redirect(conn, '/change')
