from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.shared.func import (
    get_next_page_bottom,
    html,
)
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    render_template,
)
from opennamu_forge.presentation.dependencies import get_vote_repository
async def vote_list(list_type = 'normal', num = 1):    
    votes = get_vote_repository()

    sql_num = (num * 50 - 50) if num * 50 > 0 else 0

    data = ''
    if list_type == 'normal':
        data += '<a href="/vote/list/close">(' + await get_lang('close_vote_list') + ')</a>'
        sub = 0
        data_list = votes.list_by_types(("open", "n_open"), offset=sql_num, limit=50)
    else:
        data += '<a href="/vote">(' + await get_lang('open_vote_list') + ')</a>'
        sub = '(' + await get_lang('closed') + ')'
        data_list = votes.list_by_types(("close", "n_close"), offset=sql_num, limit=50)

    data += '<ul>'

    for i in data_list:
        if list_type == 'normal':
            open_select = await get_lang('open_vote') if i.type == 'open' else await get_lang('not_open_vote')
        else:
            open_select = await get_lang('open_vote') if i.type == 'close' else await get_lang('not_open_vote')

        data += '<li><a href="/vote/' + i.vote_id + '">' + i.vote_id + '. ' + html.escape(i.name) + '</a> (' + open_select + ')</li>'

    data += '</ul>'
    menu = []
    if list_type == 'normal':
        menu = [["vote/add", await get_lang('add_vote')]] if await acl_check('', 'vote') != 1 else []
        data += await get_next_page_bottom('/vote/list/{}', num, data_list)
    else:
        data += await get_next_page_bottom('/vote/list/close/{}', num, data_list)

    return await render_template(
        await get_lang('vote_list'),
        data,
        sub,
        [['other', await get_lang('return')]] + menu
    )
