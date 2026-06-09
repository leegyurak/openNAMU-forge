from .tool.func import *

async def list_admin():
    with get_db_connect() as conn:
        user_settings = get_user_setting_repository()

        div = '<ul>'

        for data in user_settings.list_id_data_by_name_excluding_data('acl', 'user'):
            name = '' + \
                await ip_pas(data[0]) + ' ' + \
                '<a href="/auth/list/add/' + url_pas(data[1]) + '">(' + data[1] + ')</a>' + \
            ''

            div += '<li>' + name + '</li>'

        div += '</ul>'

        return await render_template(
            await get_lang('admin_list'),
            div,
            0,
            [['other', await get_lang('return')]]
        )
