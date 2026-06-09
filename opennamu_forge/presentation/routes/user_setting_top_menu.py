import html

import flask

from opennamu_forge.presentation.authorization_helpers import ban_check
from opennamu_forge.presentation.dependencies import get_user_setting_repository
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    re_error,
    redirect,
    render_template,
)
from opennamu_forge.presentation.shared.sql_dialect import ip_check, ip_or_user


async def user_setting_top_menu():
    user_settings = get_user_setting_repository()

    ip = ip_check()
    if (await ban_check(ip))[0] == 1:
        return await re_error(0)

    if ip_or_user(ip) == 1:
        return redirect('/login')
    
    if flask.request.method == 'POST':
        user_settings.upsert(ip, 'top_menu', flask.request.form.get('content', ''))

        return redirect('/change/top_menu')
    else:
        db_data = user_settings.get(ip, 'top_menu')
        
        return await render_template(
            await get_lang('user_added_menu'),
            '''
                <span>
                    EX)
                    <br>
                    ONTS
                    <br>
                    https://2du.pythonanywhere.com/
                    <br>
                    FrontPage
                    <br>
                    /w/FrontPage
                </span>
                <hr class="main_hr">
                ''' + await get_lang('not_support_skin_warning') + '''
                <hr class="main_hr">
                <form method="post">
                    <textarea class="opennamu_forge_textarea_500 __ON_TEXTAREA__" placeholder="''' + await get_lang('enter_top_menu_setting') + '''" name="content" id="content">''' + html.escape(db_data) + '''</textarea>
                    <hr class="main_hr">
                    <button class="__ON_BUTTON__" id="opennamu_forge_save_button" type="submit">''' + await get_lang('save') + '''</button>
                </form>
            ''',
            0,
            [['setting', await get_lang('return')]]
        )
