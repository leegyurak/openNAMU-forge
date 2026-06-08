from .tool.func import *

async def login_register_email():
    with get_db_connect() as conn:
        curs = conn.cursor()
        wiki_settings = get_wiki_settings_service()

        if not 'reg_id' in flask.session:
            return redirect(conn, '/register')

        if flask.request.method == 'POST':
            flask.session['reg_key'] = load_random_key(32)

            user_email = re.sub(r'\\', '', flask.request.form.get('email', ''))
            email_data = re.search(r'@([^@]+)$', user_email)
            if email_data:
                email_data = email_data.group(1)

                curs.execute(db_change(
                    "select html from html_filter where html = ? and kind = 'email'"
                ), [email_data])
                if not curs.fetchall():                
                    return redirect(conn, '/filter/email_filter')

            email_title = wiki_settings.get(SettingKey.EMAIL_TITLE)
            if email_title != '':
                t_text = html.escape(email_title)
            else:
                t_text = (await wiki_set())[0] + ' key'

            email_text = wiki_settings.get(SettingKey.EMAIL_TEXT)
            if email_text != '':
                i_text = html.escape(email_text) + '\n\nKey : ' + str(flask.session.get('reg_key'))
            else:
                i_text = 'Key : ' + str(flask.session.get('reg_key'))

            curs.execute(db_change('select id from user_set where name = "email" and data = ?'), [user_email])
            if curs.fetchall():
                return await re_error(conn, 35)

            if await send_email(conn, user_email, t_text, i_text) == 0:
                return await re_error(conn, 18)

            flask.session['reg_email'] = user_email

            return redirect(conn, '/register/email/check')
        else:
            email_insert_text = wiki_settings.get(SettingKey.EMAIL_INSERT_TEXT)
            b_text = (email_insert_text + '<hr class="main_hr">') if email_insert_text != '' else ''

            return await render_template(
                await get_lang('email'),
                '''
                    <a href="/filter/email_filter">(''' + await get_lang('email_filter_list') + ''')</a>
                    <hr class="main_hr">
                    ''' + b_text + '''
                    <form method="post">
                        <input class="__ON_INPUT__" placeholder="''' + await get_lang('email') + '''" name="email" type="text">
                        <hr class="main_hr">
                        <button class="__ON_BUTTON__" type="submit">''' + await get_lang('save') + '''</button>
                    </form>
                ''',
                0,
                [['user', await get_lang('return')]]
            )
