from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.shared.func import (
    get_default_admin_group,
    html,
)
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    render_template,
)
from opennamu_forge.presentation.dependencies import get_admin_repository
async def list_admin_group():
    admin = get_admin_repository()

    list_data = '<ul>'
    org_acl_list = get_default_admin_group()

    for data in admin.list_group_names():
        if await acl_check('', 'owner_auth', '', '') != 1 and not data in org_acl_list:
            delete_admin_group = ' <a href="/auth/list/delete/' + url_pas(data) + '">(' + await get_lang("delete") + ')</a>'
        else:
            delete_admin_group = ''

        list_data += '' + \
            '<li>' + \
                '<a href="/auth/list/add/' + url_pas(data) + '">' + html.escape(data) + '</a>' + \
                delete_admin_group + \
            '</li>' + \
        ''

    list_data += '' + \
        '</ul>' + \
        '<hr class="main_hr">' + \
        '<a href="/manager/8">(' + await get_lang('add') + ')</a>' + \
    ''

    return await render_template(
        await get_lang('admin_group_list'),
        list_data,
        0,
        [['manager', await get_lang('return')]]
    )
