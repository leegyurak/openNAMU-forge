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
from opennamu_forge.presentation.skin_helpers import load_skin


async def main_setting_main_logo():
    if await acl_check('', 'owner_auth', '', '') == 1:
        return await re_error(0)

    other_settings = get_other_setting_repository()

    skin_list = [0] + await load_skin('', 1)
    i_list = []
    for i in skin_list:
        i_list += [['logo', '' if i == 0 else i]]

    if flask.request.method == 'POST':
        for i in i_list:
            other_settings.upsert(
                i[0],
                flask.request.form.get(('main_css' if i[1] == '' else i[1]), ''),
                coverage=i[1],
            )

        await acl_check(tool = 'owner_auth', memo = 'edit_set (logo)')

        return redirect('/setting/main/logo')
    else:
        d_list = []
        for i in i_list:
            d_list += [other_settings.ensure(i[0], coverage=i[1])]

        end_data = ''
        for i in range(0, len(skin_list)):
            end_data += '' + \
                '<span>' + await get_lang('wiki_logo') + ' ' + ('(' + skin_list[i] + ')' if skin_list[i] != 0 else '') + ' (HTML)' + \
                '<hr class="main_hr">' + \
                '<input class="__ON_INPUT__" name="' + (skin_list[i] if skin_list[i] != 0 else 'main_css') + '" value="' + html.escape(d_list[i]) + '">' + \
                '<hr class="main_hr">' + \
            ''

        return await render_template(
            await get_lang('wiki_logo'),
            '''
                <form method="post">
                    ''' + end_data + '''
                    <button class="__ON_BUTTON__" id="opennamu_forge_save_button" type="submit">''' + await get_lang('save') + '''</button>
                </form>
            ''',
            0,
            [['setting/main', await get_lang('return')]]
        )
