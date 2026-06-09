from .tool.func import *

async def topic_tool_setting(topic_num = 1):
    with get_db_connect() as conn:
        topics = get_topic_repository()

        if await acl_check(tool = 'toron_auth') == 1:
            return await re_error(conn, 3)

        ip = ip_check()
        time = get_time()
        topic_num = str(topic_num)

        rd_d = topics.get_recent_discuss(topic_num)
        if rd_d is None:
            return redirect(conn, '/')

        if flask.request.method == 'POST':
            await acl_check(tool = 'toron_auth', memo = 'change_topic_set (code ' + topic_num + ')')

            stop_d = flask.request.form.get('stop_d', '')
            why_d = flask.request.form.get('why', '')
            agree_d = flask.request.form.get('agree', '')

            if stop_d != rd_d.stop:
                topics.update_recent_discuss_stop(topic_num, stop_d)

                if stop_d == 'S':
                    t_state = 'topic_state_change_stop'
                elif stop_d == 'O':
                    t_state = 'topic_state_change_close'
                else:
                    t_state = 'topic_state_change_normal'

                do_add_thread(conn, 
                    topic_num,
                    await get_lang(t_state),
                    '1'
                )

            if agree_d != rd_d.agree:
                topics.update_recent_discuss_agree(topic_num, agree_d)

                if agree_d == 'O':
                    t_state = 'topic_state_change_agree'
                else:
                    t_state = 'topic_state_change_disagree'

                do_add_thread(conn, 
                    topic_num,
                    await get_lang(t_state),
                    '1'
                )

            if why_d != '':
                do_add_thread(conn, 
                    topic_num,
                    await get_lang('why') + ' : ' + why_d,
                    '1'
                )
            
            do_reload_recent_thread(conn, 
                topic_num, 
                time
            )

            return redirect(conn, '/thread/' + topic_num)
        else:
            stop_d_list = ''
            agree_check = ''
            for_list = [
                ['O', await get_lang('topic_close')],
                ['S', await get_lang('topic_stop')],
                ['', await get_lang('topic_normal')]
            ]

            for i in for_list:
                if rd_d.stop == i[0]:
                    stop_d_list = '<option value="' + i[0] + '">' + i[1] + '</option>' + stop_d_list
                else:
                    stop_d_list += '<option value="' + i[0] + '">' + i[1] + '</option>'

            agree_check = 'checked="checked"' if rd_d.agree == 'O' else ''

            return await render_template(
                await get_lang('topic_setting'),
                await render_simple_set('''
                    <form method="post">
                        <h2>''' + await get_lang('topic_progress') + '''</h2>
                        <span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="stop_d">
                            ''' + stop_d_list + '''
                        </select></span>
                        <hr class="main_hr">
                        <label class="__ON_CHECKLABEL__"><input class="__ON_CHECKBOX__" type="checkbox" name="agree" value="O" ''' + agree_check + '''> ''' + await get_lang('topic_change_agree') + '''</label>

                        <h2>''' + await get_lang('topic_associate') + '''</h2>
                        ''' + await get_lang('topic_link_vote') + ''' (''' + await get_lang('not_working') + ''')
                        <hr class="main_hr">
                        <input class="__ON_INPUT__" placeholder="''' + await get_lang('topic_insert_vote_number') + '''" name="vote_number" type="number">

                        <h2>''' + await get_lang('why') + '''</h2>
                        <input class="__ON_INPUT__" placeholder="''' + await get_lang('why') + ''' (''' + await get_lang('markup_enabled') + ''')" name="why" type="text">
                        
                        <hr class="main_hr">
                        <button class="__ON_BUTTON__" type="submit">''' + await get_lang('save') + '''</button>
                    </form>
                '''),
                0,
                [['thread/' + topic_num + '/tool', await get_lang('return')]]
            )
