from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.shared.func import (
    do_reload_recent_thread,
    get_time,
    re_error,
)
from opennamu_forge.presentation.response_helpers import redirect
from opennamu_forge.presentation.dependencies import get_topic_repository
async def topic_comment_blind(topic_num = 1, num = 1):
    topic_num = str(topic_num)
    num = str(num)
    
    if await acl_check(tool = 'toron_auth', memo = 'blind (code ' + topic_num + '#' + num + ')') == 1:
        return await re_error(3)

    if get_topic_repository().toggle_block(topic_num, num):
        do_reload_recent_thread(
            topic_num, 
            get_time()
        )

    return redirect('/thread/' + topic_num + '#' + num)
