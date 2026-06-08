from .tool.func import *

async def recent_history_send(name = 'Test', rev = 1):
    with get_db_connect() as conn:
        num = str(rev)
        history = get_history_repository()

        if await acl_check('', 'owner_auth', '', '') == 1:
            return await re_error(conn, 3)

        if flask.request.method == 'POST':
            await acl_check(tool = 'owner_auth', memo = 'send edit ' + name + ' r' + num)

            history.update_send(name, num, flask.request.form.get('send', ''))

            return redirect(conn, '/history/' + url_pas(name))
        else:
            send = history.find_send(name, num)
            if send is not None:
                return await render_template(
                    name,
                    '''
                        <form method="post">
                            <span>''' + await get_lang('delete_warning') + '''</span>
                            <hr class="main_hr">
                            <input class="__ON_INPUT__" value="''' + html.escape(send) + '''" name="send">
                            <hr class="main_hr">
                            <button class="__ON_BUTTON__" type="submit">''' + await get_lang('edit') + '''</button>
                        </form>
                    ''',
                    '(' + await get_lang('send_edit') + ') (r' + num + ')',
                    [['history/' + url_pas(name), await get_lang('return')]]
                )
            else:
                return redirect(conn, '/history/' + url_pas(name))
