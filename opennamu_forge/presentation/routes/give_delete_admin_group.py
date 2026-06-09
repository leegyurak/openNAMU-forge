from .tool.func import *

async def give_delete_admin_group(name = 'test'):
    with get_db_connect() as conn:
        admin = get_admin_repository()
        user_settings = get_user_setting_repository()

        if name in get_default_admin_group():
            return redirect(conn, '/auth/list')

        if await acl_check('', 'owner_auth', '', '') == 1:
            return await re_error(conn, 3)

        if flask.request.method == 'POST':
            if not user_settings.data_exists('acl', name):
                await acl_check(tool = 'owner_auth', memo = 'auth list delete (' + name + ')')

                admin.delete_group(name)

                return redirect(conn, '/auth/list')
            else:
                return await re_error(conn, 47)
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
