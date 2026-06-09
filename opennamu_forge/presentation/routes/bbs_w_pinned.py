import flask

from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.dependencies import get_bbs_repository
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    redirect,
    render_simple_set,
    render_template,
)
from opennamu_forge.presentation.shared.sql_dialect import get_time

from .go_api_bbs_w import api_bbs_w


async def bbs_w_pinned(bbs_num = '', post_num = ''):
    bbs = get_bbs_repository()

    bbs_name = bbs.get_setting(str(bbs_num), "bbs_name")
    if bbs_name == "":
        return redirect('/bbs/main')
    
    bbs_num_str = str(bbs_num)
    post_num_str = str(post_num)

    if await acl_check('', 'bbs_auth', '', '') == 1:
        return redirect('/bbs/in/' + bbs_num_str)
    
    temp_dict = await api_bbs_w(bbs_num_str + '-' + post_num_str)
    if 'user_id' not in temp_dict:
        return redirect('/bbs/main')
    
    if flask.request.method == 'POST':
        if not bbs.is_pinned(bbs_num_str, post_num_str):
            bbs.add_data(bbs_num_str, 'pinned', post_num_str, get_time())
        else:
            bbs.delete_data(bbs_num_str, 'pinned', post_num_str)
        
        return redirect('/bbs/in/' + bbs_num_str)
    else:
        pinned = await get_lang('pinned') if not bbs.is_pinned(bbs_num_str, post_num_str) else await get_lang('pinned_release')

        return await render_template(
            await get_lang('bbs_post_pinned'),
            await render_simple_set('''
                <form method="post">
                    <button class="__ON_BUTTON__" type="submit">''' + pinned + '''</button>
                </form>
            '''),
            '(' + bbs_name + ')' + ' (' + post_num_str + ')',
            [['bbs/w/' + bbs_num_str + '/' + post_num_str, await get_lang('return')]]
        )
