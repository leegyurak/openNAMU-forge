from .tool.func import *

async def recent_history_hidden(name = 'Test', rev = 1):
    with get_db_connect() as conn:
        history = get_history_repository()

        num = str(rev)

        if await acl_check(tool = 'hidel_auth', memo = 'history_hidden (' + name + '#' + num + ')') != 1:
            history.toggle_hidden(name, num)

        return redirect(conn, '/history/' + url_pas(name))
