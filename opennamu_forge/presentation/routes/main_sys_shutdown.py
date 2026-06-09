from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.runtime.process_control import shutdown_current_process
from opennamu_forge.presentation.shared.func import (
    flask,
    re_error,
)
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    render_template,
)
async def main_sys_shutdown():
    if await acl_check('', 'owner_auth', '', '') == 1:
        return await re_error(3)

    if flask.request.method == 'POST':
        await acl_check(tool = 'owner_auth', memo = 'shutdown')

        shutdown_current_process()
    else:
        return await render_template(
            await get_lang('wiki_shutdown'),
            '''
                <form method="post">
                    <button class="__ON_BUTTON__" type="submit">''' + await get_lang('shutdown') + '''</button>
                </form>
            ''',
            0,
            [['manager', await get_lang('return')]]
        )
