import html

from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.dependencies import get_bbs_repository
from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.identity_helpers import ip_pas
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    redirect,
    render_template,
)


async def bbs_w(bbs_num = '', tool = 'bbs', page = 1, name = ''):
    bbs = get_bbs_repository()
    
    data = ''
    title_name = ''
    sub = ''
    bbs_name_dict = {}

    admin_auth = await acl_check(tool = 'owner_auth')
    admin_auth = 1 if admin_auth == 0 else 0

    if tool == 'bbs':
        bbs_name = bbs.get_setting(bbs_num, 'bbs_name')
        if bbs_name == '':
            return redirect('/bbs/main')
    
        bbs_num_str = str(bbs_num)

        title_name = bbs_name
        sub = '(' + await get_lang('bbs') + ')'
        menu = [['bbs/main', await get_lang('return')], ['bbs/edit/' + bbs_num_str, await get_lang('add')], ['bbs/set/' + bbs_num_str, await get_lang('bbs_set')]]
    elif tool == 'record':
        db_data = bbs.list_board_names()
        bbs_name_dict = { for_a[0] : for_a[1] for for_a in db_data } if db_data else {}
        
        title_name = name
        sub = '(' + await get_lang('bbs_record') + ')'
        menu = [['user/' + url_pas(name), await get_lang('user_tool')]]
    elif tool == 'comment_record':
        db_data = bbs.list_board_names()
        bbs_name_dict = { for_a[0] : for_a[1] for for_a in db_data } if db_data else {}
        
        title_name = name
        sub = '(' + await get_lang('bbs_comment_record') + ')'
        menu = [['user/' + url_pas(name), await get_lang('user_tool')]]
    else:
        db_data = bbs.list_board_names()
        if db_data:
            data += '<ul>'
            for for_a in db_data:
                bbs_name_dict[for_a[0]] = for_a[1]

                bbs_type = bbs.get_setting(for_a[0], 'bbs_type', default='comment')

                if bbs_type == 'thread':
                    bbs_type = await get_lang('thread_base')
                else:
                    bbs_type = await get_lang('comment_base')
                
                last_date_data = bbs.latest_board_post_date(for_a[0])
                last_date = ('(' + last_date_data + ')') if last_date_data != '' else ''

                data += '<li>'
                data += '<a href="/bbs/in/' + for_a[0] + '">' + html.escape(for_a[1]) + '</a> (' + bbs_type + ') ' + last_date
                data += '</li>'

            data += '</ul>'
        
        data += '<hr class="main_hr">'

        title_name = await get_lang('bbs_main')
        menu = [['other', await get_lang('other_tool')]] + ([['bbs/make', await get_lang('add')]] if admin_auth == 1 else [])

    if tool == 'comment_record':
        data += '''
            <table id="main_table_set">
                <tr id="main_table_top_tr">
                    <td id="main_table_width">''' + await get_lang('editor') + '''</td>
                    <td id="main_table_width">''' + await get_lang('time') + '''</td>
                    <td id="main_table_width">''' + await get_lang('comment') + '''</td>
                </tr>
        '''
    else:
        data += '''
            <table id="main_table_set">
                <tr id="main_table_top_tr">
                    <td id="main_table_width">''' + await get_lang('editor') + '''</td>
                    <td id="main_table_width">''' + await get_lang('time') + '''</td>
                    <td id="main_table_width">''' + await get_lang('last_comment_time') + '''</td>
                </tr>
        '''

    if tool == 'bbs':
        db_data = bbs.list_pinned_post_refs(bbs_num)
        db_data += bbs.list_title_post_refs(bbs_num)
    elif tool == 'record':
        db_data = bbs.list_post_refs_by_user(name)
    elif tool == 'comment_record':
        db_data = bbs.list_comment_refs_by_user(name)
    else:
        db_data = bbs.list_recent_post_refs()

    for for_b in db_data:
        db_data = bbs.list_data_rows(for_b[1], for_b[0])

        temp_dict = { for_a[0] : for_a[1] for for_a in db_data }

        bbs_name_select = ''
        bbs_split = for_b[1].split('-')
        if tool == 'comment_record':
            bbs_name_select = '(' + bbs_name_dict[bbs_split[0]] + ')'
        elif tool != 'bbs':
            bbs_name_select = '(' + bbs_name_dict[for_b[1]] + ')'

        if tool == 'bbs':
            notice = 1 if len(for_b) > 2 else 0
        else:
            notice = 0

        if tool == 'comment_record':
            temp_dict['title'] = bbs.get_data(bbs_split[0], 'title', bbs_split[1])
        
            comment_link = ''
            if len(bbs_split) > 2:
                comment_link = '-'.join(bbs_split[2:])
                
            comment_link += ('-' + for_b[0] if comment_link != '' else for_b[0])
                
            data += '''
                <tr>
                    <td>''' + await ip_pas(temp_dict['comment_user_id']) + '''</td>
                    <td>''' + temp_dict['comment_date'] + '''</td>
                    <td>''' + ('#' + comment_link) + '''</td>
                </tr>
                <tr>
                    <td colspan="3">
                        <a href="/bbs/w/''' + bbs_split[0] + '/' + bbs_split[1] + '#' + comment_link + '">' + html.escape(temp_dict['title']) + '''</a> 
                        ''' + bbs_name_select + '''
                    </td>
                </tr>
            '''
        else:
            comment_set_id = for_b[1] + '-' + for_b[0]
            comment_count = str(bbs.count_comments_for_post(comment_set_id))

            last_comment_date = bbs.latest_comment_date_for_post(comment_set_id)
        
            data += '''
                <tr class="''' + ('opennamu_forge_comment_color_red' if notice == 1 else '') + '''">
                    <td>''' + await ip_pas(temp_dict['user_id']) + '''</td>
                    <td>''' + temp_dict['date'] + '''</td>
                    <td>''' + last_comment_date + '''</td>
                </tr>
                <tr>
                    <td colspan="3">
                        <a href="/bbs/w/''' + for_b[1] + '/' + for_b[0] + '">' + html.escape(temp_dict['title']) + '''</a> 
                        (''' + comment_count + ''') 
                        ''' + bbs_name_select + '''
                    </td>
                </tr>
            '''
            
    data += '</table>'

    return await render_template(
        title_name,
        data,
        sub,
        menu
    )
