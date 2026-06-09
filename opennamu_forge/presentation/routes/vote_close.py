from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.dependencies import get_vote_repository
from opennamu_forge.presentation.response_helpers import re_error, redirect
from opennamu_forge.presentation.shared.sql_dialect import ip_check


async def vote_close(num = 1):
    num = str(num)
    
    votes = get_vote_repository()

    if await acl_check('', 'vote') == 1:
        return await re_error(0)

    vote = votes.get_main(num)
    if vote is None:
        return redirect('/vote')

    open_user = votes.get_option(num, "open_user")
    if open_user != ip_check() and await acl_check('', 'vote_auth', '', '') == 1:
        return await re_error(0)

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
        return redirect('/vote')
    else:
        return redirect('/vote/list/close')
