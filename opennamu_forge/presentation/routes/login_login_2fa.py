import flask

from opennamu_forge.presentation.authorization_helpers import ban_check
from opennamu_forge.presentation.captcha_helpers import (
    captcha_get,
    captcha_post,
)
from opennamu_forge.presentation.dependencies import get_user_setting_repository
from opennamu_forge.presentation.password_helpers import pw_check
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    http_warning,
    re_error,
    redirect,
    render_template,
)
from opennamu_forge.presentation.shared.sql_dialect import get_time, ip_check, ip_or_user
from opennamu_forge.presentation.user_agent_helpers import ua_plus


async def login_login_2fa():
    user_settings = get_user_setting_repository()

    # email 2fa
    # pw 2fa
    # q_a 2fa
    if not (flask.session and 'login_id' in flask.session):
        return redirect('/user')

    ip = ip_check()
    if ip_or_user(ip) == 0:
        return redirect('/user')

    if (await ban_check(None, 'login'))[0] == 1:
        return await re_error(0)

    if flask.request.method == 'POST':
        if await captcha_post(flask.request.form.get('g-recaptcha-response', flask.request.form.get('g-recaptcha', ''))) == 1:
            return await re_error(13)

        user_agent = flask.request.headers.get('User-Agent', '')
        user_id = flask.session['login_id']
        user_pw = flask.request.form.get('pw', '')

        user_1 = user_settings.get(user_id, "2fa_pw")
        if user_1 != "":
            user_2 = user_settings.get(user_id, "2fa_pw_encode")

            pw_check_d = pw_check(user_pw, user_1, user_2, user_id)
            if pw_check_d != 1:
                return await re_error(10)

        flask.session['id'] = user_id

        ua_plus(
            user_id, 
            ip, 
            user_agent, 
            get_time()
        )

        flask.session.pop('b_id', None)

        return redirect('/user')
    else:
        return await render_template(
            await get_lang('login'),
            '''
                    <form method="post">
                        <input class="__ON_INPUT__" placeholder="''' + await get_lang('2fa_password') + '''" name="pw" type="password">
                        <hr class="main_hr">
                        ''' + await captcha_get() + '''
                        <button class="__ON_BUTTON__" type="submit">''' + await get_lang('login') + '''</button>
                        ''' + await http_warning() + '''
                    </form>
                    ''',
            0,
            [['user', await get_lang('return')]]
        )
