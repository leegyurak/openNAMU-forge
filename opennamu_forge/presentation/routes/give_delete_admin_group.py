import flask

from opennamu_forge.presentation.admin_ui_helpers import get_default_admin_group
from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.dependencies import (
    get_admin_repository,
    get_user_setting_repository,
)
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    re_error,
    redirect,
    render_template,
)


async def give_delete_admin_group(name = 'test'):
    admin = get_admin_repository()
    user_settings = get_user_setting_repository()

    if name in get_default_admin_group():
        return redirect('/auth/list')

    if await acl_check('', 'owner_auth', '', '') == 1:
        return await re_error(3)

    if flask.request.method == 'POST':
        if not user_settings.data_exists('acl', name):
            await acl_check(tool = 'owner_auth', memo = 'auth list delete (' + name + ')')

            admin.delete_group(name)

            return redirect('/auth/list')
        else:
            return await re_error(47)
    else:
        return await render_template(
            await get_lang("delete_admin_group"),
            '' + \
                '<form method="post">' + \
                    '<button class="__ON_BUTTON__" type="submit">' + await get_lang('delete') + '</button>' + \
                '</form>' + \
            '',
            '(' + name + ')',
            [['auth/list', await get_lang('return')]]
        )
