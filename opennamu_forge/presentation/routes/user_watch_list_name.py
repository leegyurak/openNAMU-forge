from .tool.func import *

async def user_watch_list_name(tool, name = 'Test'):
    with get_db_connect() as conn:
        user_settings = get_user_setting_repository()

        ip = ip_check()
        if ip_or_user(ip) != 0:
            return redirect(conn, '/login')
        
        name_from = 0
        if tool == 'watch_list_from':
            name_from = 1
            tool = 'watch_list'
        elif tool == 'star_doc_from':
            name_from = 1
            tool = 'star_doc'

        if tool == 'watch_list':
            type_data = 'watchlist'
        else:
            type_data = 'star_doc'

        if user_settings.exists_data(ip, type_data, name):
            user_settings.delete_data(ip, type_data, name)
        else:
            if tool == 'watch_list':
                if user_settings.count_by_name(ip, type_data) > 10:
                    return await re_error(conn, 28)

            user_settings.upsert(ip, type_data, name)

        if name_from == 1:
            return redirect(conn, '/w/' + url_pas(name))
        else:
            if tool == 'watch_list':
                return redirect(conn, '/watch_list')
            else:
                return redirect(conn, '/star_doc')
