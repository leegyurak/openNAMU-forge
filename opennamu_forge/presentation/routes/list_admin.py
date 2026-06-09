from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.identity_helpers import ip_pas
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    render_template,
)
from opennamu_forge.presentation.dependencies import get_user_setting_repository
async def list_admin():
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
