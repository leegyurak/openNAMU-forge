from opennamu_forge.presentation.dependencies import get_user_setting_repository
from opennamu_forge.presentation.identity_helpers import ip_pas
from opennamu_forge.presentation.pagination_helpers import get_next_page_bottom
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    render_template,
)


async def list_user(arg_num = 1):
    user_settings = get_user_setting_repository()

    sql_num = (arg_num * 50 - 50) if arg_num * 50 > 0 else 0

    list_data = '<ul>'

    user_list = user_settings.list_id_data_by_name_ordered_by_data_desc('date', offset=sql_num, limit=50)
    for data in user_list:
        list_data += '<li>'
        list_data += await ip_pas(data[0])
        list_data += ' | ' + data[1] if data[1] != '' else ''
        list_data += '</li>'

    list_data += '</ul>' + await get_next_page_bottom('/list/user/{}', arg_num, user_list)

    return await render_template(
        await get_lang('member_list'),
        list_data,
        0,
        [['other', await get_lang('return')]]
    )
