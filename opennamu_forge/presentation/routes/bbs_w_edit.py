import html

import flask

from opennamu_forge.presentation.admin_ui_helpers import get_acl_list
from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.captcha_helpers import captcha_post
from opennamu_forge.presentation.dependencies import get_bbs_repository
from opennamu_forge.presentation.edit_validation_helpers import do_edit_filter
from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    re_error,
    redirect,
    render_simple_set,
    render_template,
)
from opennamu_forge.presentation.shared.sql_dialect import get_time, ip_check

from .edit import edit_editor
from .go_api_bbs_w import api_bbs_w
from .go_api_bbs_w_comment_one import api_bbs_w_comment_one


async def bbs_w_edit(bbs_num = '', post_num = '', comment_num = ''):
    bbs = get_bbs_repository()

    bbs_num_str = str(bbs_num)
    post_num_str = str(post_num)

    ip = ip_check()

    if bbs.get_setting(bbs_num_str, 'bbs_name') == '':
        return redirect('/bbs/main')
    
    if comment_num != '':
        temp_dict = await api_bbs_w_comment_one(bbs_num_str + '-' + post_num_str + '-' + comment_num)
        if 'comment_user_id' in temp_dict:
            if not temp_dict['comment_user_id'] == ip and await acl_check('', 'owner_auth', '', '') == 1:
                return await re_error(0)
        else:
            return redirect('/bbs/main')
    elif post_num != '':
        temp_dict = await api_bbs_w(bbs_num_str + '-' + post_num_str)
        if 'user_id' in temp_dict:
            if not temp_dict['user_id'] == ip and await acl_check('', 'owner_auth', '', '') == 1:
                return await re_error(0)
        else:
            return redirect('/bbs/main')
        
    if await acl_check(bbs_num_str, 'bbs_edit') == 1:
        return redirect('/bbs/set/' + bbs_num_str)
    
    i_list = ['post_view_acl', 'post_comment_acl']

    if flask.request.method == 'POST':
        if await captcha_post(flask.request.form.get('g-recaptcha-response', flask.request.form.get('g-recaptcha', ''))) == 1:
            return await re_error(13)
    
        if post_num == '':
            latest_code = bbs.latest_data_code(bbs_num_str, 'title')
            id_data = str(latest_code + 1) if latest_code else '1'
        else:
            id_data = post_num_str

        title = flask.request.form.get('title', 'test')
        title = 'test' if title == '' else title
        data = flask.request.form.get('content', '')
        if data == '':
            # re_error로 대체 예정
            return redirect('/bbs/in/' + bbs_num_str)
        
        if await do_edit_filter(title) == 1:
            return await re_error(21)

        if await do_edit_filter(data) == 1:
            return await re_error(21)
        
        date = get_time()

        if comment_num != '':
            sub_code = (bbs_num_str + '-' + post_num_str + '-' + comment_num).split('-')
            sub_code_last = ''
            if len(sub_code) > 2:
                sub_code_last = sub_code[len(sub_code) - 1]
                del sub_code[len(sub_code) - 1]
                
            sub_code = '-'.join(sub_code)

            bbs.update_data(sub_code, 'comment', sub_code_last, data)
        elif post_num == '':
            bbs.add_data(bbs_num_str, 'title', id_data, title)
            bbs.add_data(bbs_num_str, 'data', id_data, data)
            bbs.add_data(bbs_num_str, 'date', id_data, date)
            bbs.add_data(bbs_num_str, 'user_id', id_data, ip)
        else:
            bbs.update_data(bbs_num_str, 'title', post_num, title)
            bbs.update_data(bbs_num_str, 'data', id_data, data)
            bbs.update_data(bbs_num_str, 'date', id_data, date)

        if comment_num != '':
            return redirect('/bbs/w/' + bbs_num_str + '/' + id_data + '#' + url_pas(comment_num))
        else:
            return redirect('/bbs/w/' + bbs_num_str + '/' + id_data)
    else:
        option_display = ''

        if comment_num != '':
            temp_dict = await api_bbs_w_comment_one(bbs_num_str + '-' + post_num_str + '-' + comment_num)

            title = ''
            data = temp_dict['comment']
            option_display = 'display: none;'
        elif post_num == '':
            title = ''
            data = ''
        else:
            temp_dict = await api_bbs_w(bbs_num_str + '-' + post_num_str)

            title = temp_dict['title']
            data = temp_dict['data']

        acl_div = ['' for _ in range(0, len(i_list))]
        acl_list = await get_acl_list()
        for for_a in range(0, len(i_list)):
            for data_list in acl_list:
                acl_div[for_a] += '<option value="' + data_list + '">' + (data_list if data_list != '' else 'normal') + '</option>'

        editor_top_text = '<a href="/filter/edit_filter">(' + await get_lang('edit_filter_rule') + ')</a>'

        if editor_top_text != '':
            editor_top_text += '<hr class="main_hr">'

        if comment_num != '':
            bbs_title = await get_lang('bbs_comment_edit')
        elif post_num == '':
            bbs_title = await get_lang('post_add')
        else:
            bbs_title = await get_lang('post_edit')

        return await render_template(
            bbs_title,
            editor_top_text + '''
                <form method="post">                        
                    <input class="__ON_INPUT__" style="''' + option_display + '''" placeholder="''' + await get_lang('title') + '''" name="title" value="''' + html.escape(title) + '''">
                    <hr style="''' + option_display + '''" class="main_hr">

                    ''' + await edit_editor(ip, data, 'bbs') + '''

                    <!--
                    <div style="''' + option_display + '''">
                        ''' + await render_simple_set('''
                            <hr class="main_hr">
                            <a href="/acl/TEST#exp">(''' + await get_lang('reference') + ''')</a>
                            <h2>''' + await get_lang('acl') + '''</h2>
                            <h3>''' + await get_lang('post_view_acl') + '''</h3>
                            <span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="post_view_acl">''' + acl_div[0] + '''</select></span>

                            <h4>''' + await get_lang('post_comment_acl') + '''</h4>
                            <span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="post_comment_acl">''' + acl_div[1] + '''</select></span>

                            <h2>''' + await get_lang('markup') + '''</h2>
                            ''' + await get_lang('not_working') + '''
                        ''') + '''
                    </div>
                    -->
                </form>
            ''',
            0,
            [['bbs/in/' + bbs_num_str, await get_lang('return')]]
        )
