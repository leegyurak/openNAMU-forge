from .tool.func import *

async def list_user_check(name = 'test', plus_name = None, arg_num = 1, do_type = 'normal'):
    with get_db_connect() as conn:
        user_agents = get_user_agent_repository()

        plus_id = plus_name

        check_type = do_type if do_type in ['simple', 'normal'] else 'normal'
        check_type = '' if check_type == 'normal' else check_type

        num = arg_num
        sql_num = (num * 50 - 50) if num * 50 > 0 else 0

        if await acl_check(tool = 'all_admin_auth', ip = name) != 1 or (plus_id and await acl_check(tool = 'all_admin_auth', ip = plus_id) != 1):
            if await acl_check('', 'owner_auth', '', '') == 1:
                return await re_error(conn, 4)

        div = ''

        if await acl_check(tool = 'check_auth', memo = (check_type + ' ' if check_type != '' else '') + 'check (' + name + ')') == 1:
            return await re_error(conn, 3)

        if check_type == '':
            if ip_or_user(name) == 0:
                user_settings = get_user_setting_repository()
                approval_question = user_settings.get(name, 'approval_question')
                if approval_question:
                    approval_question_answer = user_settings.get(name, 'approval_question_answer')
                    if approval_question_answer:
                        div += '''
                            <table id="main_table_set">
                                <tbody>
                                    <tr id="main_table_top_tr">
                                        <td>Q</td>
                                        <td>''' + approval_question + '''</td>
                                        <td>A</td>
                                        <td>''' + approval_question_answer + '''</td>
                                    </tr>
                                </tbody>
                            </table>
                            <hr class="main_hr">
                        '''

            if plus_id:
                name_column = 'ip' if ip_or_user(name) == 1 else 'name'
                plus_column = 'ip' if ip_or_user(plus_id) == 1 else 'name'

                if num == 1:
                    all_ip_count = user_agents.count_distinct_ips_by_two_identities(name_column, name, plus_column, plus_id)
                    a_ip_count = user_agents.count_distinct_ips_by_identity(name_column, name)
                    b_ip_count = user_agents.count_distinct_ips_by_identity(plus_column, plus_id)

                    if a_ip_count + b_ip_count != all_ip_count:
                        div += await get_lang('same_ip_exist') + '<hr class="main_hr">'    

                record = user_agents.list_by_two_identities(name_column, name, plus_column, plus_id, offset=sql_num)
            else:
                name_column = 'ip' if ip_or_user(name) == 1 else 'name'
                record = user_agents.list_by_identity(name_column, name, offset=sql_num)

            if record:
                if not plus_id:
                    div = '' + \
                        '<a href="/manager/14/' + url_pas(name) + '">(' + await get_lang('compare') + ')</a> ' + \
                        '<a href="/list/user/check/' + url_pas(name) + '/simple">(' + await get_lang('simple_check') + ')</a>' + \
                        '<hr class="main_hr">' + \
                    '' + div
                else:
                    div = '' + \
                        '<a href="/list/user/check/' + url_pas(name) + '">(' + name + ')</a> ' + \
                        '<a href="/list/user/check/' + url_pas(plus_id) + '">(' + plus_id + ')</a>' + \
                        '<hr class="main_hr">' + \
                    '' + div

                div += '''
                    <table id="main_table_set">
                        <tbody>
                            <tr id="main_table_top_tr">
                                <td id="main_table_width">''' + await get_lang('name') + '''</td>
                                <td id="main_table_width">''' + await get_lang('ip') + '''</td>
                                <td id="main_table_width">''' + await get_lang('time') + '''</td>
                            </tr>
                '''

                set_n = 0
                for data in record:
                    if data.ua:
                        if len(data.ua) > 300:
                            ua = '' + \
                                '<a href="javascript:void();" onclick="document.getElementById(\'check_' + str(set_n) + '\').style.display=\'block\';">(300+)</a>' + \
                                '<div id="check_' + str(set_n) + '" style="display:none;">' + html.escape(data.ua) + '</div>' + \
                            ''
                            set_n += 1
                        else:
                            ua = html.escape(data.ua)
                    else:
                        ua = '<br>'

                    div += '''
                        <tr>
                            <td>
                                <a href="/list/user/check/''' + url_pas(data.name) + '''">''' + data.name + '''</a>
                                <a href="/list/user/check/delete/''' + url_pas(data.name) + '/' + url_pas(data.ip) + '/' + url_pas(data.today) + '/' + ('0' if ip_or_user(name) == 0 else '1') + '''">
                                    (''' + await get_lang('delete') + ''')
                                </a>
                            </td>
                            <td><a href="/list/user/check/''' + url_pas(data.ip) + '''">''' + data.ip + '''</a></td>
                            <td>''' + data.today + '''</td>
                        </tr>
                        <tr>
                            <td colspan="3">''' + ua + '''</td>
                        </tr>
                    '''

                div += '''
                        </tbody>
                    </table>
                '''

            if plus_id:
                div += await get_next_page_bottom(
                    '/list/user/check/' + url_pas(name) + '/normal/{}/' + url_pas(plus_id), 
                    num, 
                    record
                )
            else:
                div += await get_next_page_bottom(
                    '/list/user/check/' + url_pas(name) + '/normal/{}', 
                    num, 
                    record
                )

            if plus_id:
                name += ', ' + plus_id

            return await render_template(
                name,
                div,
                '(' + await get_lang('check') + ')',
                [['manager', await get_lang('return')]]
            )
        else:
            value_column = 'name' if ip_or_user(name) == 1 else 'ip'
            identity_column = 'ip' if ip_or_user(name) == 1 else 'name'
            record = user_agents.list_distinct_values_by_identity(value_column, identity_column, name, offset=sql_num)

            div = ''
            for for_a in record:
                div += '<li><a href="/list/user/check/' + url_pas(for_a) + '/simple">' + for_a + '</a></li>'

            if div != '':
                div = '<ul>' + div + '</ul>'
                div += await get_next_page_bottom(
                    '/list/user/check/' + url_pas(name) + '/' + check_type + '/{}', 
                    num, 
                    record
                )

            div = '' + \
                '<a href="/list/user/check/' + url_pas(name) + '/normal">(' + await get_lang('check') + ')</a>' + \
            '' + div

            return await render_template(
                name,
                div,
                '(' + await get_lang('simple_check') + ')',
                [['check/' + url_pas(name), await get_lang('return')]]
            )
