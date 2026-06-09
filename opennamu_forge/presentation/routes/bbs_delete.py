from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.shared.func import (
    flask,
)
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    redirect,
    render_simple_set,
    render_template,
)
from opennamu_forge.presentation.dependencies import get_bbs_repository
async def bbs_delete(bbs_num = ''):
    bbs = get_bbs_repository()

    bbs_name = bbs.get_setting(str(bbs_num), "bbs_name")
    if bbs_name == "":
        return redirect('/bbs/main')
    
    bbs_num_str = str(bbs_num)

    if await acl_check('', 'owner_auth', '', '') == 1:
        return redirect('/bbs/in/' + bbs_num_str)
    
    if bbs_num_str == 0:
        return redirect('/bbs/in/' + bbs_num_str)
    
    if flask.request.method == 'POST':
        bbs.delete_board(bbs_num_str)
        
        return redirect('/bbs/main')
    else:
        return await render_template(
            await get_lang('bbs_delete'),
            await render_simple_set('''
                <form method="post">
                    <span>''' + await get_lang('delete_warning') + '''</span>
                    <hr class="main_hr">
                    <button class="__ON_BUTTON__" type="submit">''' + await get_lang('delete') + '''</button>
                </form>
            '''),
            '(' + bbs_name + ')',
            [['bbs/set/' + bbs_num_str, await get_lang('return')]]
        )
