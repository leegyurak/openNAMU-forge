from opennamu_forge.presentation.authorization_helpers import ban_check
from opennamu_forge.presentation.shared.func import (
    SettingKey,
    flask,
    ip_check,
    ip_or_user,
    pw_check,
    pw_encode,
    re_error,
)
from opennamu_forge.presentation.text_helpers import number_check
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    http_warning,
    redirect,
    render_template,
)
from opennamu_forge.presentation.dependencies import (
    get_user_setting_repository,
    get_wiki_settings_service,
)
async def user_setting_pw():
    wiki_settings = get_wiki_settings_service()
    user_settings = get_user_setting_repository()

    if (await ban_check())[0] == 1:
        return await re_error(0)

    ip = ip_check()
    if ip_or_user(ip) != 0:
        return redirect('/login')

    if flask.request.method == 'POST':
        user_pw_now = flask.request.form.get('password_now', '')
        user_pw = flask.request.form.get('password_new', '')
        user_repeat = flask.request.form.get('password_new_repeat', '')
    
        # PW 검증
        if user_pw == '':
            return await re_error(27)

        if user_pw != user_repeat:
            return await re_error(20)

        # PW 길이 제한
        password_min_length_raw = wiki_settings.get(SettingKey.PASSWORD_MIN_LENGTH)
        if password_min_length_raw != '':
            password_min_length = int(number_check(password_min_length_raw))
            if password_min_length > len(user_pw):
                return await re_error(40)

        db_user_pw = user_settings.get(ip, "pw")
        if db_user_pw == "":
            return await re_error(2)
            
        db_user_encode = user_settings.get(ip, "encode")
        if db_user_encode == "":
            return await re_error(2)
            
        if pw_check(user_pw_now, db_user_pw, db_user_encode, ip) != 1:
            return await re_error(10)

        user_settings.upsert(ip, "pw", pw_encode(user_pw))

        return redirect('/user')
    else:
        password_min_length_raw = wiki_settings.get(SettingKey.PASSWORD_MIN_LENGTH)
        if password_min_length_raw != '':
            password_min_length = ' (' + await get_lang('password_min_length') + ' : ' + password_min_length_raw + ')'
        else:
            password_min_length = ''
        
        return await render_template(
            await get_lang('password_change'),
            '''
                <form method="post">
                    <input class="__ON_INPUT__" placeholder="''' + await get_lang('now_password') + '''" name="password_now" type="password">
                    <hr class="main_hr">
                    
                    <input class="__ON_INPUT__" placeholder="''' + await get_lang('new_password') + password_min_length + '''" name="password_new" type="password">
                    <hr class="main_hr">
                    
                    <input class="__ON_INPUT__" placeholder="''' + await get_lang('password_confirm') + '''" name="password_new_repeat" type="password">
                    <hr class="main_hr">
                    
                    <button class="__ON_BUTTON__" type="submit">''' + await get_lang('save') + '''</button>
                    
                    ''' + await http_warning() + '''
                </form>
            ''',
            0,
            [['change', await get_lang('return')]]
        )
