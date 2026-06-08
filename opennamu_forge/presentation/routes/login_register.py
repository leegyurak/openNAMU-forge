from .tool.func import *

async def login_register():
    with get_db_connect() as conn:
        curs = conn.cursor()
        wiki_settings = get_wiki_settings_service()

        if (await ban_check(None, 'register'))[0] == 1:
            return await re_error(conn, 0)

        ip = ip_check()
        admin = await acl_check(tool = 'owner_auth')
        admin = 1 if admin == 0 else 0

        if admin != 1 and ip_or_user(ip) == 0:
            return redirect(conn, '/user')

        if admin != 1:
            if wiki_settings.enabled(SettingKey.REG):
                return await re_error(conn, 0)

        if flask.request.method == 'POST':
            # 리캡차
            if await captcha_post(conn, flask.request.form.get('g-recaptcha-response', flask.request.form.get('g-recaptcha', ''))) == 1:
                return await re_error(conn, 13)

            user_id = flask.request.form.get('id', '')
            user_pw = flask.request.form.get('pw', '')
            user_repeat = flask.request.form.get('pw2', '')

            # PW 검증
            if user_id == '' or user_pw == '':
                return await re_error(conn, 27)

            if user_pw != user_repeat:
                return await re_error(conn, 20)
            
            # ID와 PW 동일성 검증
            if user_id == user_pw:
                return await re_error(conn, 49)

            # PW 길이 제한
            password_min_length_raw = wiki_settings.get(SettingKey.PASSWORD_MIN_LENGTH)
            if password_min_length_raw != '':
                password_min_length = int(number_check(password_min_length_raw))
                if password_min_length > len(user_pw):
                    return await re_error(conn, 40)

            if do_user_name_check(conn, user_id) == 1:
                return await re_error(conn, 8)

            if admin != 1:
                # 이메일 필요시 /register/email로 발송
                if wiki_settings.get(SettingKey.EMAIL_HAVE) != '':
                    # 임시로 세션에 저장
                    flask.session['reg_id'] = user_id
                    flask.session['reg_pw'] = user_pw

                    return redirect(conn, '/register/email')

                # 가입 승인 필요시 /register/submit으로 발송
                if wiki_settings.get(SettingKey.REQUIRES_APPROVAL) != '':
                    flask.session['submit_id'] = user_id
                    flask.session['submit_pw'] = user_pw

                    return redirect(conn, '/register/submit')

            # 전부 아니면 바로 가입 후 /login으로 발송
            add_user(conn, user_id, user_pw)

            return redirect(conn, '/login')
        else:
            contract_text = wiki_settings.get(SettingKey.CONTRACT)
            contract = (contract_text + '<hr class="main_hr">') if contract_text != '' else ''

            password_min_length_raw = wiki_settings.get(SettingKey.PASSWORD_MIN_LENGTH)
            if password_min_length_raw != '':
                password_min_length = ' (' + await get_lang('password_min_length') + ' : ' + password_min_length_raw + ')'
            else:
                password_min_length = ''

            return await render_template(
                await get_lang('register'),
                '''
                    <form method="post">
                        ''' + contract + '''

                        <input class="__ON_INPUT__" placeholder="''' + await get_lang('id') + '''" name="id" type="text">
                        <hr class="main_hr">

                        <input class="__ON_INPUT__" placeholder="''' + await get_lang('password') + password_min_length + '''" name="pw" type="password">
                        <hr class="main_hr">

                        <input class="__ON_INPUT__" placeholder="''' + await get_lang('password_confirm') + '''" name="pw2" type="password">
                        <hr class="main_hr">

                        ''' + await captcha_get(conn) + '''

                        <button class="__ON_BUTTON__" type="submit">''' + await get_lang('save') + '''</button>

                        ''' + await http_warning() + '''
                    </form>
                ''',
                0,
                [['user', await get_lang('return')]]
            )
