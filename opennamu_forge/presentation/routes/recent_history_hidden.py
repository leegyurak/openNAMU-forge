from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.response_helpers import redirect
from opennamu_forge.presentation.dependencies import get_history_repository
async def recent_history_hidden(name = 'Test', rev = 1):
    history = get_history_repository()

    num = str(rev)

    if await acl_check(tool = 'hidel_auth', memo = 'history_hidden (' + name + '#' + num + ')') != 1:
        history.toggle_hidden(name, num)

    return redirect('/history/' + url_pas(name))
