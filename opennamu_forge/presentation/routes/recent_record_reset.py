import flask

from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.dependencies import get_history_repository
from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    re_error,
    redirect,
    render_template,
)


async def recent_record_reset(name = 'Test'):
    history = get_history_repository()

    if await acl_check('', 'owner_auth', '', '') == 1:
        return await re_error(3)

    if flask.request.method == 'POST':
        await acl_check(tool = 'owner_auth', memo = 'record reset ' + name)

        history.delete_by_ip(name)

        return redirect('/record/' + url_pas(name))
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
            '(' + await get_lang('record_reset') + ')',
            [['record/' + url_pas(name), await get_lang('return')]]
        )
