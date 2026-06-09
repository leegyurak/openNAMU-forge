from .tool.func import *

async def recent_record_reset(name = 'Test'):
    with get_db_connect() as conn:
        history = get_history_repository()

        if await acl_check('', 'owner_auth', '', '') == 1:
            return await re_error(conn, 3)

        if flask.request.method == 'POST':
            await acl_check(tool = 'owner_auth', memo = 'record reset ' + name)

            history.delete_by_ip(name)

            return redirect(conn, '/record/' + url_pas(name))
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
