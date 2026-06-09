from .tool.func import *

def recent_change_send_render(data):
    def send_render_href_replace(match):
        match = match.group(1)
        data_unescape = html.unescape(match)

        return '<a href="/w/' + url_pas(data_unescape) + '">' + match + '</a>'
    
    def send_render_link(match):
        link_main = match[2]
        link_main = link_main.replace('"', '&quot;')

        return match[1] + '<a href="' + link_main + '">' + link_main + '</a>'

    if data == '&lt;br&gt;' or data == '' or re.search(r'^ +$', data):
        data = '<br>'
    else:
        data = data.replace('javascript:', '')

        data = re.sub(r'( |^)(https?:\/\/(?:[^ ]+))', send_render_link, data)
        data = re.sub(r'&lt;a(?:(?:(?!&gt;).)*)&gt;((?:(?!&lt;\/a&gt;).)+)&lt;\/a&gt;', send_render_href_replace, data)

    return data

async def recent_change(name = '', tool = '', num = 1, set_type = 'normal'):
    with get_db_connect() as conn:
        history = get_history_repository()

        ip = ip_check()
        
        all_admin = await acl_check(tool = 'all_admin_auth', ip = ip)
        all_admin = 1 if all_admin == 0 else 0

        owner = await acl_check(tool = 'owner_auth', ip = ip)
        owner = 1 if owner == 0 else 0

        option_list = [
            ['normal', await get_lang('normal')],
            ['edit', await get_lang('edit')],
            ['move', await get_lang('move')],
            ['delete', await get_lang('delete')],
            ['revert', await get_lang('revert')],
            ['r1', await get_lang('new_doc')],
            ['edit_request', await get_lang('edit_request')],
            ['file', await get_lang('file')],
            ['category', await get_lang('category')]
        ]
        if tool == 'history':
            option_list += [['setting', await get_lang('setting')]]

        if flask.request.method == 'POST':
            return redirect(conn, '/diff/' + flask.request.form.get('b', '1') + '/' + flask.request.form.get('a', '1') + '/' + url_pas(name))
        else:
            ban = ''
            select = ''
            sub = ''
            admin = owner
            div = '''
                <table id="main_table_set">
                    <tbody>
                        <tr id="main_table_top_tr">
            '''

            sql_num = (num * 50 - 50) if num * 50 > 0 else 0

            if tool == 'history':
                div += '''
                    <td id="main_table_width">''' + await get_lang('version') + '''</td>
                    <td id="main_table_width">''' + await get_lang('editor') + '''</td>
                    <td id="main_table_width">''' + await get_lang('time') + '''</td>
                '''
                sub = '(' + await get_lang('history') + ')'

                set_type = '' if set_type == 'edit' else set_type
                if set_type != 'normal':
                    data_list = history.list_records_by_title_type(name, set_type, offset=sql_num)
                else:
                    data_list = history.list_records_by_title(name, offset=sql_num)
            elif tool == 'record':
                div +=  '''
                    <td id="main_table_width">''' + await get_lang('document_name') + '''</td>
                    <td id="main_table_width">''' + await get_lang('editor') + '''</td>
                    <td id="main_table_width">''' + await get_lang('time') + '''</td>
                '''
                sub = '(' + await get_lang('edit_record') + ')'
                set_type = '' if set_type == 'edit' else set_type

                if set_type != 'normal':
                    data_list = history.list_records_by_ip_type(name, set_type, offset=sql_num)
                else:
                    data_list = history.list_records_by_ip(name, offset=sql_num)
            else:
                div +=  '''
                    <td id="main_table_width">''' + await get_lang('document_name') + '''</td>
                    <td id="main_table_width">''' + await get_lang('editor') + '''</td>
                    <td id="main_table_width">''' + await get_lang('time') + '''</td>
                '''
                sub = ''
                set_type = '' if set_type == 'edit' else set_type

                data_list = []

                if num == 1 or all_admin != 1:
                    data_list = history.list_recent_change_records_by_type(set_type)
                else:
                    if set_type != 'normal':
                        data_list = history.list_records_by_type(set_type, offset=sql_num)
                    else:
                        data_list = history.list_records(offset=sql_num)

            div += '</tr>'

            all_ip = await ip_pas([i.author for i in data_list])
            for data in data_list:
                select += '<option value="' + data.revision_id + '">' + data.revision_id + '</option>'
                send = data.send

                if re.search(r"\+", data.length):
                    leng = '<span style="color:green;">(' + data.length + ')</span>'
                elif re.search(r"\-", data.length):
                    leng = '<span style="color:red;">(' + data.length + ')</span>'
                else:
                    leng = '<span style="color:gray;">(' + data.length + ')</span>'

                ip = all_ip[data.author]
                m_tool = '<a href="/history_tool/' + data.revision_id + '/' + url_pas(data.title) + '">(' + await get_lang('tool') + ')</a>'

                style = ['', '']
                date = data.date

                type_data = ''
                if data.change_type != '':
                    if data.change_type == 'r1':
                        type_data = ' (' + data.change_type + ')'
                    else:
                        type_data = ' (' + await get_lang(data.change_type) + ')'

                send += type_data

                if data.hide == 'O':
                    if admin == 1:
                        style[0] = 'class="opennamu_forge_history_blind"'
                        style[1] = 'class="opennamu_forge_history_blind"'
                    else:
                        ip = ''
                        ban = ''
                        date = ''
                        send = ''

                        style[0] = 'style="display: none;"'
                        style[1] = 'class="opennamu_forge_history_blind"'

                if tool == 'history':
                    if int(data.revision_id) < 2:
                        title = '<a href="/raw_rev/' + data.revision_id + '/' + url_pas(name) + '">r' + data.revision_id + '</a> '
                    else:
                        title = '<a href="/diff/' + str(int(data.revision_id) - 1) + '/' + data.revision_id + '/' + url_pas(name) + '">r' + data.revision_id + '</a> '
                else:
                    title = '<a href="/w/' + url_pas(data.title) + '">' + html.escape(data.title) + '</a> '
                    if int(data.revision_id) < 2:
                        title += '<a href="/history/' + url_pas(data.title) + '">(r' + data.revision_id + ')</a> '
                    else:
                        title += '<a href="/diff/' + str(int(data.revision_id) - 1) + '/' + data.revision_id + '/' + url_pas(data.title) + '">(r' + data.revision_id + ')</a> '

                div += '''
                    <tr ''' + style[0] + '''>
                        <td>''' + title + m_tool + ' ' + leng + '''</td>
                        <td>''' + ip + ban + '''</td>
                        <td>''' + date + '''</td>
                    </tr>
                    <tr ''' + style[1] + '''>
                        <td colspan="3">''' + recent_change_send_render(html.escape(send)) + '''</td>
                    </tr>
                '''

            div += '''
                    </tbody>
                </table>
            '''

            set_type = 'edit' if set_type == '' else set_type
            if tool == 'history':
                div = '' + \
                    ' '.join(['<a href="/history_page/1/' + for_a[0] + '/' + url_pas(name) + '">(' + for_a[1] + ')</a> ' for for_a in option_list]) + \
                    '<hr class="main_hr">' + div + \
                ''
                menu = [['w/' + url_pas(name), await get_lang('return')]]

                if set_type == 'normal':
                    div = '''
                        <form method="post">
                            <span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="a">''' + select + '''</select></span> <span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="b">''' + select + '''</select></span>
                            <button class="__ON_BUTTON__" type="submit">''' + await get_lang('compare') + '''</button>
                        </form>
                        <hr class="main_hr">
                    ''' + div

                if admin == 1:
                    menu += [
                        ['history_add/' + url_pas(name), await get_lang('history_add')],
                        ['history_reset/' + url_pas(name), await get_lang('history_reset')]
                    ]

                title = name
                div += await get_next_page_bottom('/history_page/{}/' + set_type + '/' + url_pas(name), num, data_list)
            elif tool == 'record':
                div = '' + \
                    ' '.join(['<a href="/record/1/' + for_a[0] + '/' + url_pas(name) + '">(' + for_a[1] + ')</a> ' for for_a in option_list]) + \
                    '<hr class="main_hr">' + div + \
                ''

                title = name
                menu = [['user/' + url_pas(name), await get_lang('user_tool')]]
                if admin == 1:
                    menu += [['record/reset/' + url_pas(name), await get_lang('record_reset')]]

                div += await get_next_page_bottom('/record/{}/' + url_pas(set_type) + '/' + url_pas(name), num, data_list)
            else:
                div = '' + \
                    ' '.join(['<a href="/recent_change/1/' + for_a[0] + '">(' + for_a[1] + ')</a> ' for for_a in option_list]) + \
                    '<a href="/recent_change/1/user">(' + await get_lang('user_document') + ')</a> ' + \
                    '<hr class="main_hr">' + div + \
                ''

                menu = [['other', await get_lang('return')], ['recent_edit_request', await get_lang('edit_request')]]
                title = await get_lang('recent_change')

                if all_admin == 1:
                    div += await get_next_page_bottom('/recent_change/{}/' + set_type, num, data_list)

            if sub == '':
                sub = 0

            return await render_template(
                title,
                div,
                sub,
                menu
            )
