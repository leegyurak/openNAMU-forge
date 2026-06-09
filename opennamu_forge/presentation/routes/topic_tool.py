from .tool.func import *

async def topic_tool(topic_num = 1):
    with get_db_connect() as conn:
        topics = get_topic_repository()

        data = ''
        topic_num = str(topic_num)

        close_data = topics.get_recent_discuss(topic_num)
        if close_data is not None:
            if close_data.stop == 'S':
                t_state = await get_lang('topic_stop')
            elif close_data.stop == 'O':
                t_state = await get_lang('topic_close')
            else:
                t_state = await get_lang('topic_normal')
                
            if close_data.agree == 'O':
                t_state += ' (' + await get_lang('topic_agree') + ')'
        else:
            t_state = await get_lang('topic_normal')

        acl_state = close_data.acl if close_data is not None and close_data.acl != '' else 'normal'
        
        thread_view_acl = topics.get_thread_setting(topic_num, 'thread_view_acl')
        acl_view_state = thread_view_acl if thread_view_acl != '' else 'normal'

        if await acl_check(tool = 'toron_auth') != 1:
            data = '''
                <h2>''' + await get_lang('admin_tool') + '''</h2>
                <ul>
                    <li><a href="/thread/''' + topic_num + '/setting">' + await get_lang('topic_setting') + '''</a></li>
                    <li><a href="/thread/''' + topic_num + '/acl">' + await get_lang('topic_acl_setting') + '''</a></li>
                </ul>
            '''
        data += '''
            <h2>''' + await get_lang('tool') + '''</h2>
            <ul>
                <li>''' + await get_lang('topic_state') + ''' : ''' + t_state + '''</li>
                <li>''' + await get_lang('topic_acl') + ''' : <a href="/acl/TEST#exp">''' + acl_state + '''</a></li>
                <li>''' + await get_lang('topic_view_acl') + ''' : <a href="/acl/TEST#exp">''' + acl_view_state + '''</a></li>
            </ul>
        '''

        if await acl_check(tool = 'owner_auth') != 1:
            data += '''
                <h2>''' + await get_lang('owner') + '''</h2>
                <ul>
                    <li>
                        <a href="/thread/''' + topic_num + '''/delete">
                            ''' + await get_lang('topic_delete') + '''
                        </a>
                    </li>
                    <li>
                        <a href="/thread/''' + topic_num + '''/change">
                            ''' + await get_lang('topic_name_change') + '''
                        </a>
                    </li>
                </ul>
            '''

        return await render_template(
            await get_lang('topic_tool'),
            data,
            0,
            [['thread/' + topic_num, await get_lang('return')]]
        )
