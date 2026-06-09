import flask

from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.dependencies import get_user_agent_repository
from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    re_error,
    redirect,
    render_template,
)


async def list_user_check_delete(name = None, ip = None, time = None, do_type = 1):
    user_agents = get_user_agent_repository()

    if await acl_check('', 'owner_auth', '', '') == 1:
        return await re_error(4)

    user_id = name
    user_ip = ip
    return_type = do_type

    if user_id and user_ip and time:
        if flask.request.method == 'POST':
            user_agents.delete(user_id, user_ip, time)

            return redirect('/list/user/check/' + url_pas(user_id if return_type == '0' else user_ip))
        else:
            return await render_template(
                await get_lang('check'),
                '''
                    ''' + await get_lang('name') + ''' : ''' + user_id + '''
                    <hr class="main_hr">
                    ''' + await get_lang('ip') + ''' : ''' + user_ip + '''
                    <hr class="main_hr">
                    ''' + await get_lang('time') + ''' : ''' + time + '''
                    <hr class="main_hr">
                    <form method="post">
                        <button class="__ON_BUTTON__" type="submit">''' + await get_lang('delete') + '''</button>
                    </form>
                ''',
                '(' + await get_lang('delete') + ')',
                [['check/' + url_pas(user_id if return_type == '0' else user_ip), await get_lang('return')]]
            )
    else:
        return redirect()
