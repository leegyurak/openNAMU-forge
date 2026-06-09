from .tool.func import *

async def topic_tool_delete(topic_num = 1):
    with get_db_connect() as conn:
        topics = get_topic_repository()

        if await acl_check(tool = 'owner_auth') == 1:
            return await re_error(conn, 3)

        topic_num = str(topic_num)

        if flask.request.method == 'POST':
            await acl_check(tool = 'owner_auth', memo = 'delete topic (' + topic_num + ')')

            topics.delete_thread(topic_num)

            return redirect(conn, '/')
        else:
            return await render_template(
                await get_lang('topic_delete'),
                '''
                    <form method="post">
                        <span>''' + await get_lang('delete_warning') + '''</span>
                        <hr class="main_hr">
                        <button class="__ON_BUTTON__" type="submit">''' + await get_lang('delete') + '''</button>
                    </form>
                ''',
                0,
                [['thread/' + topic_num + '/tool', await get_lang('return')]]
            )
