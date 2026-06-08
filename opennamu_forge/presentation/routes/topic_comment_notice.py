from .tool.func import *

async def topic_comment_notice(topic_num = 1, num = 1):
    with get_db_connect() as conn:
        topic_num = str(topic_num)
        num = str(num)
        
        if await acl_check(tool = 'toron_auth', memo = 'notice (code ' + topic_num + '#' + num + ')') == 1:
            return await re_error(conn, 3)

        if get_topic_repository().toggle_top(topic_num, num):
            do_reload_recent_thread(conn, 
                topic_num, 
                get_time()
            )

        return redirect(conn, '/thread/' + topic_num + '#' + num)
