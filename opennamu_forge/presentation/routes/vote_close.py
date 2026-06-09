from .tool.func import *

async def vote_close(num = 1):
    num = str(num)
    
    with get_db_connect() as conn:
        votes = get_vote_repository()

        if await acl_check('', 'vote') == 1:
            return await re_error(conn, 0)

        vote = votes.get_main(num)
        if vote is None:
            return redirect(conn, '/vote')

        open_user = votes.get_option(num, "open_user")
        if open_user != ip_check() and await acl_check('', 'vote_auth', '', '') == 1:
            return await re_error(conn, 0)

        if vote.type == 'close':
            type_set = 'open'
        elif vote.type == 'n_close':
            type_set = 'n_open'
        elif vote.type == 'open':
            type_set = 'close'
        else:
            type_set = 'n_close'

        votes.update_main_type(num, vote.type, type_set)
        votes.delete_option(num, "end_date")

        if vote.type == 'close' or vote.type == 'n_close':
            return redirect(conn, '/vote')
        else:
            return redirect(conn, '/vote/list/close')
