from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.dependencies import get_discussion_service, get_topic_repository
from opennamu_forge.presentation.response_helpers import re_error, redirect
from opennamu_forge.presentation.shared.sql_dialect import get_time


async def topic_comment_blind(topic_num = 1, num = 1):
    topic_num = str(topic_num)
    num = str(num)
    
    if await acl_check(tool = 'toron_auth', memo = 'blind (code ' + topic_num + '#' + num + ')') == 1:
        return await re_error(3)

    if get_topic_repository().toggle_block(topic_num, num):
        get_discussion_service().reload_recent_thread(
            topic_num, 
            get_time()
        )

    return redirect('/thread/' + topic_num + '#' + num)
