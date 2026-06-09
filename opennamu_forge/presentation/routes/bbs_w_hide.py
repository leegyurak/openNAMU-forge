import flask

from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.dependencies import get_bbs_repository
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    redirect,
    render_simple_set,
    render_template,
)


async def bbs_w_hide(bbs_num = '', post_num = ''):
    bbs = get_bbs_repository()

    bbs_name = bbs.get_setting(str(bbs_num), "bbs_name")
    if bbs_name == "":
        return redirect('/bbs/main')
    
    bbs_num_str = str(bbs_num)
    post_num_str = str(post_num)

    if await acl_check('', 'bbs_auth', '', '') == 1:
        return redirect('/bbs/in/' + bbs_num_str)
    
    if flask.request.method == 'POST':
        pass
    else:
        return await render_template(
            await get_lang('bbs_post_hide'),
            await render_simple_set('''
                <form method="post">
                    <button class="__ON_BUTTON__" type="submit">''' + await get_lang('hide') + '''</button>
                </form>
            '''),
            '(' + bbs_name + ')' + ' (' + post_num_str + ')',
            [['bbs/w/' + bbs_num_str + '/' + post_num_str, await get_lang('return')]]
        )
