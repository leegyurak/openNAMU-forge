from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    render_template,
)
from opennamu_forge.presentation.dependencies import get_history_repository
async def recent_history_tool(name = 'Test', rev = 1):
    history = get_history_repository()

    num = str(rev)

    data = '' + \
        '<h2>' + await get_lang('tool') + '</h2>' + \
        '<ul>' + \
            '<li><a href="/raw_rev/' + num + '/' + url_pas(name) + '">' + await get_lang('raw') + '</a></li>' + \
    ''

    data += '<li><a href="/revert/' + num + '/' + url_pas(name) + '">' + await get_lang('revert') + ' (r' + num + ')</a></li>'
    if rev - 1 > 0:
        data += '<li><a href="/revert/' + str(rev - 1) + '/' + url_pas(name) + '">' + await get_lang('revert') + ' (r' + str(rev - 1) + ')</a></li>'

    if rev - 1 > 0:
        data += '<li><a href="/diff/' + str(rev - 1) + '/' + num + '/' + url_pas(name) + '">' + await get_lang('compare') + '</a></li>'

    data += '<li><a href="/history/' + url_pas(name) + '">' + await get_lang('history') + '</a></li>'
    data += '</ul>'

    if await acl_check(tool = 'hidel_auth') != 1:
        data += '<h3>' + await get_lang('admin') + '</h3>'
        data += '<ul>'
        data += '<li><a href="/history_hidden/' + num + '/' + url_pas(name) + '">'
        if history.is_hidden(name, num):
            data += await get_lang('hide_release') 
        else:
            data += await get_lang('hide')

        data += '</a></li>'
        data += '</ul>'

    if await acl_check('', 'owner_auth', '', '') != 1:
        data += '<h3>' + await get_lang('owner') + '</h3>'
        data += '<ul>'
        data += '<li><a href="/history_delete/' + num + '/' + url_pas(name) + '">' + await get_lang('history_delete') + '</a></li>'
        data += '<li><a href="/history_send/' + num + '/' + url_pas(name) + '">' + await get_lang('send_edit') + '</a></li>'
        data += '</ul>'

    return await render_template(
        name,
        data,
        '(r' + num + ')',
        [['history/' + url_pas(name), await get_lang('return')]]
    )
