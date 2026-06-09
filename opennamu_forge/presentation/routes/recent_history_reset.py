from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.shared.func import (
    flask,
    re_error,
)
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    redirect,
    render_template,
)
from opennamu_forge.presentation.dependencies import get_history_repository
async def recent_history_reset(name = 'Test'):
    history = get_history_repository()

    if await acl_check('', 'owner_auth', '', '') == 1:
        return await re_error(3)

    if flask.request.method == 'POST':
        await acl_check(tool = 'owner_auth', memo = 'history reset ' + name)

        history.delete_title(name)

        return redirect('/history/' + url_pas(name))
    else:
        return await render_template(
            name,
            '''
                <form method="post">
                    <span>''' + await get_lang('delete_warning') + '''</span>
                    <hr class="main_hr">
                    <button class="__ON_BUTTON__" type="submit">''' + await get_lang('reset') + '''</button>
                </form>
            ''',
            '(' + await get_lang('history_reset') + ')',
            [['history/' + url_pas(name), await get_lang('return')]]
        )
