import html

import flask

from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.dependencies import get_other_setting_repository
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    re_error,
    redirect,
    render_template,
)


async def main_setting_top_menu():
    other_settings = get_other_setting_repository()

    if await acl_check('', 'owner_auth', '', '') == 1:
        return await re_error(0)
    
    if flask.request.method == 'POST':
        other_settings.upsert('top_menu', flask.request.form.get('content', ''))

        await acl_check(tool = 'owner_auth', memo = 'edit_set (top_menu)')

        return redirect('/setting/top_menu')
    else:
        db_data = other_settings.get('top_menu')
        
        return await render_template(
            await get_lang('top_menu_setting'),
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
