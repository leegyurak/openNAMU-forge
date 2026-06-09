import html

import flask

from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.captcha_helpers import captcha_post
from opennamu_forge.presentation.dependencies import get_bbs_repository, get_discussion_service
from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.golang_gateway import python_to_golang
from opennamu_forge.presentation.identity_helpers import ip_pas
from opennamu_forge.presentation.rendering.render_helpers import render_set
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    re_error,
    redirect,
    render_template,
)
from opennamu_forge.presentation.shared.sql_dialect import get_time, ip_check, re
from opennamu_forge.presentation.text_helpers import cache_v

from .edit import edit_editor
from .go_api_bbs_w import api_bbs_w
from .go_api_topic import api_topic_thread_pre_render


async def bbs_w_post(bbs_num = '', post_num = ''):
    bbs = get_bbs_repository()

    bbs_name = bbs.get_setting(bbs_num, 'bbs_name')
    if bbs_name == '':
        return redirect('/bbs/main')

    bbs_num_str = str(bbs_num)
    post_num_str = str(post_num)
    bbs_comment_acl = await acl_check(bbs_num_str, 'bbs_comment')
    ip = ip_check()

    temp_dict = await api_bbs_w(bbs_num_str + '-' + post_num_str)
    if temp_dict == {}:
        return redirect('/bbs/main')
    
    bbs_type = bbs.get_setting(bbs_num, 'bbs_type')
    if bbs_type == '':
        return redirect('/bbs/main')
    else:
        if flask.request.method == 'POST':
            if bbs_type == 'thread':
                if bbs_comment_acl == 1:
                    return redirect('/bbs/set/' + bbs_num_str)
                
                if await captcha_post(flask.request.form.get('g-recaptcha-response', flask.request.form.get('g-recaptcha', ''))) == 1:
                    return await re_error(13)

                set_id = bbs_num_str + '-' + post_num_str

                latest_code = bbs.latest_data_code(set_id, 'comment')
                id_data = str(latest_code + 1) if latest_code else '1'

                data = flask.request.form.get('content', '')
                if data == '':
                    # re_error로 대체 예정
                    return redirect('/bbs/w/' + bbs_num_str + '/' + post_num_str)
                
                data = data.replace('\r', '')
                data = await api_topic_thread_pre_render(data, id_data, ip, set_id, bbs_name, temp_dict['title'], 'post')
                
                date = get_time()

                bbs.add_data(set_id, 'comment', id_data, data)
                bbs.add_data(set_id, 'comment_date', id_data, date)
                bbs.add_data(set_id, 'comment_user_id', id_data, ip)

                await get_discussion_service().add_alarm(temp_dict['user_id'], ip, 'BBS <a href="/bbs/w/' + bbs_num_str + '/' + post_num_str + '#' + id_data + '">' + html.escape(bbs_name) + ' - ' + html.escape(temp_dict['title']) + '#' + id_data + '</a>')

                return redirect('/bbs/w/' + bbs_num_str + '/' + post_num_str + '#' + id_data)
            else:
                if bbs_comment_acl == 1:
                    return redirect('/bbs/set/' + bbs_num_str)
                
                if await captcha_post(flask.request.form.get('g-recaptcha-response', flask.request.form.get('g-recaptcha', ''))) == 1:
                    return await re_error(13)
                
                select = flask.request.form.get('comment_select', '0')
                select = '' if select == '0' else select

                comment_user_name = ''

                if select != '':
                    select_split = select.split('-')
                    if len(select_split) < 2:
                        comment_user_name = bbs.get_data(bbs_num_str + '-' + post_num_str, 'comment_user_id', select_split[0])
                        if comment_user_name == '':
                            # re_error로 변경 예정
                            return redirect('/bbs/w/' + bbs_num_str + '/' + post_num_str)
                        else:
                            set_id = bbs_num_str + '-' + post_num_str + '-' + select_split[0]
                    else:
                        comment_user_name = bbs.get_data(
                            bbs_num_str + '-' + post_num_str + '-' + '-'.join(select_split[0:len(select_split) - 1]),
                            'comment_user_id',
                            select_split[len(select_split) - 1],
                        )
                        if comment_user_name == '':
                            return redirect('/bbs/w/' + bbs_num_str + '/' + post_num_str)
                        else:
                            set_id = bbs_num_str + '-' + post_num_str + '-' + '-'.join(select_split)
                else:
                    set_id = bbs_num_str + '-' + post_num_str

                latest_code = bbs.latest_data_code(set_id, 'comment')
                id_data = str(latest_code + 1) if latest_code else '1'

                data = flask.request.form.get('content', '')
                if data == '':
                    # re_error로 대체 예정
                    return redirect('/bbs/w/' + bbs_num_str + '/' + post_num_str)

                date = get_time()

                bbs.add_data(set_id, 'comment', id_data, data)
                bbs.add_data(set_id, 'comment_date', id_data, date)
                bbs.add_data(set_id, 'comment_user_id', id_data, ip)
            
                if set_id == '':
                    end_id = id_data
                else:
                    set_id = re.sub(r'^[0-9]+-[0-9]+-?', '', set_id)
                    set_id += '-' if set_id != '' else ''
                    end_id = set_id + id_data

                await get_discussion_service().add_alarm(temp_dict['user_id'], ip, 'BBS <a href="/bbs/w/' + bbs_num_str + '/' + post_num_str + '#' + end_id + '">' + html.escape(bbs_name) + ' - ' + html.escape(temp_dict['title']) + '#' + end_id + '</a>')
                if comment_user_name != '':
                    await get_discussion_service().add_alarm(comment_user_name, ip, 'BBS <a href="/bbs/w/' + bbs_num_str + '/' + post_num_str + '#' + end_id + '">' + html.escape(bbs_name) + ' - ' + html.escape(temp_dict['title']) + '#' + end_id + '</a>')

                return redirect('/bbs/w/' + bbs_num_str + '/' + post_num_str + '#' + end_id)
        else:
            if await acl_check(bbs_num_str, 'bbs_view') == 1:
                return await re_error(0)

            date = ''
            date += '<a href="javascript:opennamu_forge_change_comment(\'0\');">(' + await get_lang('comment') + ')</a> '
            date += temp_dict['date']

            data = '<div class="opennamu_forge_bbs_w_post_tab">'
            data += '<big><big><big>' + html.escape(temp_dict['title']) + '</big></big></big>'
            data += '<hr class="main_hr">'
            data += await ip_pas(temp_dict['user_id']) + '<span style="float: right;">' + date + '</span>'
            data += '<hr>'
            data += '<div class="opennamu_forge_bbs_w_post_tab_content">' + await render_set(doc_data = temp_dict['data']) + '</div>'
            data += '</div>'

            if bbs_comment_acl == 0:
                data += '<hr class="main_hr">'
                data += '<div id="opennamu_forge_bbs_w_post_tabom"></div>'

            data += '' + \
                '<hr>' + \
                '<div id="opennamu_forge_bbs_w_post"></div>' + \
                '<script defer src="/views/main_css/js/route/topic.js' + cache_v() + '"></script>' + \
                '<script defer src="/views/main_css/js/route/bbs_w_post.js' + cache_v() + '"></script>' + \
                '<script>window.addEventListener("DOMContentLoaded", function() { opennamu_forge_load_comment(); });</script>' + \
            ''

            bbs_comment_form = ''
            if bbs_comment_acl == 0:
                bbs_comment_form += '''
                    <div id="opennamu_forge_bbs_w_post_select"></div>
                    ''' + await edit_editor(ip, '', 'bbs_comment') + '''
                '''

            data += '''
                <form method="post">
                    ''' + bbs_comment_form + '''
                </form>
            '''
            
            await python_to_golang("get_json", path = "v2/bbs/w/page_view_post/" + url_pas(bbs_num_str) + "/" + url_pas(post_num_str))

            view_count_data = await python_to_golang("get_json", path = "v2/bbs/w/page_view/" + url_pas(bbs_num_str) + "/" + url_pas(post_num_str))
            view_count = view_count_data['data']

            return await render_template(
                bbs_name,
                data,
                '(' + await get_lang('bbs') + ')',
                [['bbs/in/' + bbs_num_str, await get_lang('return')], ['bbs/edit/' + bbs_num_str + '/' + post_num_str, await get_lang('edit')], ['bbs/tool/' + bbs_num_str + '/' + post_num_str, await get_lang('tool')]],
                [temp_dict['date'], 0, 0, view_count],
            )
