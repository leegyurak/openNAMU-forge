import flask

from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.dependencies import get_history_mutation_service
from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    re_error,
    redirect,
    render_template,
)
from opennamu_forge.presentation.shared.sql_dialect import get_time, ip_check

from .edit import edit_editor


async def recent_history_add(name = 'Test', do_type = ''):

    ip = ip_check()
    if await acl_check('', 'owner_auth', '', '') == 1:
        return await re_error(0)

    if flask.request.method == 'POST':
        await acl_check(tool = 'owner_auth', memo = 'history_add (' + name + ')')

        today = get_time()
        content = flask.request.form.get('content', '')
        leng = '+' + str(len(content))

        get_history_mutation_service().add_history(
            name,
            content,
            today,
            'Add:' + flask.request.form.get('get_ip', ''),
            flask.request.form.get('send', ''),
            leng,
            mode = 'add'
        )

        return redirect('/history/' + url_pas(name))
    else:            
        return await render_template(
            await get_lang('history_add'),
            '''
                <form method="post">
                    <input class="__ON_INPUT__" placeholder="''' + await get_lang('why') + '''" name="send">
                    <hr class="main_hr">
                    
                    <input class="__ON_INPUT__" placeholder="''' + await get_lang('name') + '''" name="get_ip">
                    <hr class="main_hr">

                    ''' + await edit_editor(ip) + '''
                </form>
            ''',
            '(' + name + ')',
            [['history/' + url_pas(name), await get_lang('return')]]
        )
