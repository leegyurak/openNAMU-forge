from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.runtime.go_process import terminate_go_process
from opennamu_forge.presentation.runtime.process_control import schedule_restart
from opennamu_forge.presentation.shared.func import (
    flask,
    re_error,
)
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    render_template,
)

async def main_sys_restart(golang_process):
    if await acl_check('', 'owner_auth', '', '') == 1:
        return await re_error(3)

    if flask.request.method == 'POST':
        await acl_check(tool = 'owner_auth', memo = 'restart')

        terminate_go_process(golang_process)
        schedule_restart()
        return flask.Response(await get_lang("warning_restart"), status = 200)
    else:
        return await render_template(
            await get_lang('wiki_restart'),
            '''
                <form method="post">
                    <button class="__ON_BUTTON__" type="submit">''' + await get_lang('restart') + '''</button>
                </form>
            ''',
            0,
            [['manager', await get_lang('return')]]
        )
