from .tool.func import *

async def user_setting_email_check():
    with get_db_connect() as conn:
        curs = conn.cursor()
        wiki_settings = get_wiki_settings_service()

        ip = ip_check()
        if ip_or_user(ip) != 0:
            return redirect(conn, '/login')

        re_set_list = ['c_key', 'c_email']
        if  not 'c_key' in flask.session or \
            not 'c_email' in flask.session:
            for i in re_set_list:
                flask.session.pop(i, None)

        if  flask.request.method == 'POST':
            ip = ip_check()
            input_key = flask.request.form.get('key', '')
            user_agent = flask.request.headers.get('User-Agent', '')

            if flask.session['c_key'] == input_key:
                curs.execute(db_change('delete from user_set where name = "email" and id = ?'), [ip])
                curs.execute(db_change('insert into user_set (name, id, data) values ("email", ?, ?)'), [ip, flask.session['c_email']])

            for i in re_set_list:
                flask.session.pop(i, None)

            return redirect(conn, '/change')
        else:
            check_key_text = wiki_settings.get(SettingKey.CHECK_KEY_TEXT)
            b_text = (check_key_text + '<hr class="main_hr">') if check_key_text != '' else ''

            return await render_template(
                await get_lang('check_key'),
                '''
                    <form method="post">
                        ''' + b_text + '''
                        <input class="__ON_INPUT__" placeholder="''' + await get_lang('key') + '''" name="key" type="text">
                        <hr class="main_hr">
                        <button class="__ON_BUTTON__" type="submit">''' + await get_lang('save') + '''</button>
                    </form>
                ''',
                0,
                [['user', await get_lang('return')]]
            )
