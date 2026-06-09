from .tool.func import *

async def topic_comment_tool(topic_num = 1, num = 1):
    with get_db_connect() as conn:
        topics = get_topic_repository()
        
        num = str(num)
        topic_num = str(topic_num)
        
        if await acl_check('', 'topic_view', topic_num) == 1:
            return await re_error(conn, 0)

        data = topics.get(topic_num, num)
        if data is None:
            return redirect(conn, '/thread/' + topic_num)

        ban = '''
            <h2>''' + await get_lang('state') + '''</h2>
            <ul>
                <li>''' + await get_lang('writer') + ' : ''' + await ip_pas(data.author) + '''</li>
                <li>''' + await get_lang('time') + ' : ' + data.date + '''</li>
            </ul>
            <h2>''' + await get_lang('other_tool') + '''</h2>
            <ul>
                <li>
                    <a href="/thread/''' + topic_num + '/comment/' + num + '''/raw">''' + await get_lang('raw') + '''</a>
                </li>
            </ul>
        '''

        if await acl_check(tool = 'toron_auth') != 1:
            ban += '''
                <h2>''' + await get_lang('admin_tool') + '''</h2>
                <ul>
                    <li>
                        <a href="/auth/ban/''' + url_pas(data.author) + '''">
                            ''' + (await get_lang('ban') + ' | ' + await get_lang('release')) + '''
                        </a>
                    </li>
                    <li>
                        <a href="/thread/''' + topic_num + '''/comment/''' + num + '''/blind">
                            ''' + (await get_lang('hide') + ' | ' + await get_lang('hide_release')) + '''
                        </a>
                    </li>
                    <li>
                        <a href="/thread/''' + topic_num + '''/comment/''' + num + '''/notice">
                            ''' + (await get_lang('pinned') + ' | ' + await get_lang('pinned_release')) + '''
                        </a>
                    </li>
                    <li>
                        <a href="/thread/''' + topic_num + '''/comment/''' + num + '''/delete">
                            ''' + await get_lang('delete') + '''
                        </a>
                </ul>
            '''

        return await render_template(
            await get_lang('discussion_tool'),
            ban,
            '(#' + num + ')',
            [['thread/' + topic_num + '#' + num, await get_lang('return')]]
        )
