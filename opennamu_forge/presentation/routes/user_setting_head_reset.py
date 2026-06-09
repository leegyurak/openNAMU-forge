from .tool.func import *

async def user_setting_head_reset():
    with get_db_connect() as conn:
        user_settings = get_user_setting_repository()

        skin_name = await skin_check(1)
        ip = ip_check()

        if flask.request.method == 'POST':
            get_data = ''
            if ip_or_user(ip) == 0:
                user_settings.upsert(ip, 'custom_css', get_data)
                user_settings.upsert(ip, 'custom_css_' + skin_name, get_data)

            flask.session['head'] = ''
            flask.session['head_' + skin_name] = ''

            return redirect(conn, '/change/head')
        else:
            if ip_or_user(ip) == 0:
                data = user_settings.get(ip, 'custom_css')
                data_skin = user_settings.get(ip, 'custom_css_' + skin_name)
            else:
                data = flask.session['head'] if 'head' in flask.session else ''
                data_skin = flask.session['head_' + skin_name] if 'head_' + skin_name in flask.session else ''
            
            return '''
                <form method="post">
                    <style>.main_hr { border: none; }</style>
                    ''' + await get_lang('all') + '''
                    <hr class="main_hr">
                    <pre>''' + html.escape(data) + '''</pre>
                    <hr class="main_hr">
                    ''' + skin_name + '''
                    <hr class="main_hr">
                    <pre>''' + html.escape(data_skin) + '''</pre>
                    <hr class="main_hr">
                    <button class="__ON_BUTTON__" type="submit">''' + await get_lang('reset') + '''</button>
                </form>
            '''
