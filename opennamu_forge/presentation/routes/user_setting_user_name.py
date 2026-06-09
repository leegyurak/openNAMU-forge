from .tool.func import *

async def user_setting_user_name(user_name = ''):
    with get_db_connect() as conn:
        user_settings = get_user_setting_repository()

        ip = ip_check()
        if user_name != '':
            if await acl_check('', 'owner_auth', '', '') == 1:
                return await re_error(conn, 3)
            else:
                ip = user_name
    
        if ip_or_user(ip) == 0:
            if flask.request.method == 'POST':
                auto_data = ['user_name', flask.request.form.get('new_user_name', '')]
                if do_user_name_check(conn, auto_data[1]) == 1:
                    return await re_error(conn, 8)

                user_settings.upsert(ip, auto_data[0], auto_data[1])

                if user_name != '':
                    return redirect(conn, '/change/user_name/' + url_pas(user_name))
                else:
                    return redirect(conn, '/change/user_name')
            else:
                user_name = ip

                db_data = user_settings.get(ip, 'user_name')
                if db_data != '':
                    user_name = db_data

                return await render_template(
                    await get_lang('change_user_name'),
                    '''
                        <form method="post">
                            <input class="__ON_INPUT__" name="new_user_name" placeholder="''' + await get_lang('user_name') + '''" value="''' + html.escape(user_name) + '''">
                            <hr class="main_hr">
                            <button class="__ON_BUTTON__" id="opennamu_forge_save_button" type="submit">''' + await get_lang('save') + '''</button>
                        </form>
                    ''',
                    0,
                    [['change', await get_lang('return')]]
                )
        else:
            return redirect(conn, '/login')
