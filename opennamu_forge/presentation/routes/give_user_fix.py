from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.shared.func import (
    flask,
    html,
    pw_encode,
    re_error,
)
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    redirect,
    render_template,
)
from opennamu_forge.presentation.dependencies import get_user_setting_repository
async def give_user_fix(user_name = ''):
    user_settings = get_user_setting_repository()

    if not user_settings.exists(user_name, 'pw'):
        return await re_error(2)

    if await acl_check('', 'owner_auth', '', '') == 1:
        return await re_error(3)

    if flask.request.method == 'POST':
        select = flask.request.form.get('select', '')

        await acl_check(tool = 'owner_auth', memo = 'user_fix (' + user_name + ') (' + select + ')')
        if select == 'password_change':
            password = flask.request.form.get('new_password', '')
            check_password = flask.request.form.get('password_check', '')

            if password == check_password:
                hashed = pw_encode(password)
                user_settings.upsert(user_name, 'pw', hashed)
            else:
                return await re_error(20)
        elif select == '2fa_password_change':
            password = flask.request.form.get('new_password', '')
            check_password = flask.request.form.get('password_check', '')

            if password == check_password:
                hashed = pw_encode(password)
                user_settings.upsert(user_name, '2fa_pw', hashed)
            else:
                return await re_error(20)
        elif select == '2fa_off':
            if user_settings.exists(user_name, '2fa'):
                user_settings.upsert(user_name, '2fa', '')

        return redirect('/user/' + url_pas(user_name))
    else:
        return await render_template(
            await get_lang('user_fix'),
            '''
                <form method="post">
                    <div id="opennamu_forge_get_user_info">''' + html.escape(user_name) + '''</div>
                    <hr class="main_hr">
                    <a href="/change/user_name/''' + url_pas(user_name) + '''">(''' + await get_lang('change_user_name') + ''')</a>
                    <hr class="main_hr">
                    <span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="select">
                        <option value="password_change">''' + await get_lang('password_change') + '''</option>
                        <option value="2fa_password_change">''' + await get_lang('2fa_password_change') + '''</option>
                        <option value="2fa_off">''' + await get_lang('2fa_off') + '''</option>
                    </select></span>
                    <hr class="main_hr">
                    ''' + await get_lang('password_change') + ''' | ''' + await get_lang('2fa_password_change') + '''
                    <hr class="main_hr">
                    <input class="__ON_INPUT__" placeholder="''' + await get_lang('new_password') + '''" name="new_password" type="password">
                    <hr class="main_hr">
                    <input class="__ON_INPUT__" placeholder="''' + await get_lang('password_confirm') + '''" name="password_check" type="password">
                    <hr class="main_hr">
                    <button class="__ON_BUTTON__" type="submit">''' + await get_lang('go') + '''</button>
                </form>
            ''',
            0,
            [['manager', await get_lang('return')]]
        )
