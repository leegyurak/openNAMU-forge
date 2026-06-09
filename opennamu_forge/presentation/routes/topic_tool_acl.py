from .tool.func import *

async def topic_tool_acl(topic_num = 1):
    with get_db_connect() as conn:
        topics = get_topic_repository()

        if await acl_check(tool = 'toron_auth') == 1:
            return await re_error(conn, 3)

        ip = ip_check()
        time = get_time()
        topic_num = str(topic_num)

        rd_d = topics.get_recent_discuss(topic_num)
        if not rd_d:
            return redirect(conn, '/')

        if flask.request.method == 'POST':
            await acl_check(tool = 'toron_auth', memo = 'topic_acl_set (code ' + topic_num + ')')

            topic_check = topics.latest_comment_id(topic_num)
            if topic_check:
                acl_data = flask.request.form.get('acl', '')
                acl_data_view = flask.request.form.get('acl_view', '')

                topics.update_recent_discuss_acl(topic_num, acl_data)
                
                topics.upsert_thread_setting(topic_num, 'thread_view_acl', acl_data_view)

                do_add_thread(conn, 
                    topic_num,
                    await get_lang('acl_thread_change') + ' : ' + acl_data,
                    '1'
                )
                do_reload_recent_thread(conn, 
                    topic_num, 
                    time
                )

            return redirect(conn, '/thread/' + topic_num)
        else:
            acl_list = await get_acl_list()
            acl_html_list = ''
            acl_html_list_view = ''

            topic_acl_get = rd_d.acl
            for data_list in acl_list:
                if topic_acl_get == data_list:
                    check = 'selected="selected"'
                else:
                    check = ''

                acl_html_list += '<option value="' + data_list + '" ' + check + '>' + (data_list if data_list != '' else 'normal') + '</option>'

            db_data = topics.get_thread_setting(topic_num, 'thread_view_acl')
            for data_list in acl_list:
                if db_data == data_list:
                    check = 'selected="selected"'
                else:
                    check = ''

                acl_html_list_view += '<option value="' + data_list + '" ' + check + '>' + (data_list if data_list != '' else 'normal') + '</option>'

            return await render_template(
                await get_lang('topic_acl_setting'),
                '''
                    <form method="post">
                        <a href="/acl/TEST#exp">(''' + await get_lang('reference') + ''')</a>
                        <h2>''' + await get_lang('thread_acl') + '''</h2>
                        <span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="acl">
                            ''' + acl_html_list + '''
                        </select></span>
                        <h2>''' + await get_lang('view_acl') + ''' (''' + await get_lang('beta') + ''')</h2>
                        <span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="acl_view">
                            ''' + acl_html_list_view + '''
                        </select></span>
                        <hr class="main_hr">
                        <button class="__ON_BUTTON__" type="submit">''' + await get_lang('save') + '''</button>
                    </form>
                ''',
                0,
                [['thread/' + topic_num + '/tool', await get_lang('return')]]
            )
