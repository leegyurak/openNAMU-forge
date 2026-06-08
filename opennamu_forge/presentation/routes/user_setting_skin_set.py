from .tool.func import *

async def user_setting_skin_set():
    with get_db_connect() as conn:
        data = flask.make_response(await re_error(conn, 5))

        main_data = get_other_setting_repository().get("language")
        user_data = get_user_setting_repository().get(ip_check(), "lang", default=main_data)

        data.set_cookie('language', main_data)
        data.set_cookie('user_language', user_data)

        return data
