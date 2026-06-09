import html

import flask

from opennamu_forge.presentation.dependencies import get_html_filter_repository
from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    redirect,
    render_template,
)
from opennamu_forge.presentation.text_helpers import get_tool_js_safe


async def main_tool_redirect(num = 1, add_2 = ''):
    html_filters = get_html_filter_repository()

    title_list = {
        0 : [await get_lang('document_name'), '/acl', await get_lang('document_setting')],
        1 : [0, '/list/user/check', await get_lang('check')],
        2 : [await get_lang('file_name'), '/filter/file_filter/add', await get_lang('file_filter_add')],
        3 : [0, '/auth/give', await get_lang('authorize')],
        4 : [0, '/user', await get_lang('user_tool')],
        6 : [await get_lang('name'), '/auth/list/add', await get_lang('add_admin_group')],
        7 : [await get_lang('name'), '/filter/edit_filter/add', await get_lang('edit_filter_add')],
        8 : [await get_lang('document_name'), '/search', await get_lang('search')],
        9 : [0, '/recent_block/user', await get_lang('blocked_user')],
        10 : [0, '/recent_block/admin', await get_lang('blocked_admin')],
        11 : [await get_lang('document_name'), '/watch_list', await get_lang('add_watchlist')],
        12 : [await get_lang('compare_target'), '/list/user/check', await get_lang('compare_target')],
        13 : [await get_lang('document_name'), '/edit', await get_lang('load')],
        14 : [await get_lang('document_name'), '/star_doc', await get_lang('add_star_doc')],
        16 : [0, '/auth/give/fix', await get_lang('user_fix')],
        17 : [await get_lang('search'), '/recent_block/all/1', await get_lang('search')],
    }
    
    if num == 1:
        return redirect('/manager')
    
    # 이전 버전 잔재로 -2부터 시작
    num -= 2
    if num not in title_list:
        return redirect()

    add_1 = flask.request.form.get('name', 'test')
    if flask.request.method == 'POST':
        if add_2 != '':
            if num != 12:
                flask.session['edit_load_document'] = add_1
                return redirect('/edit_from/' + url_pas(add_2))
            else:
                return redirect(title_list[num][1] + '/' + url_pas(add_2) + '/normal/1/' + url_pas(add_1))
        else:
            return redirect(title_list[num][1] + '/' + url_pas(add_1))
    else:
        if title_list[num][0] == 0:
            placeholder = await get_lang('user_name')
        else:
            placeholder = title_list[num][0]

        top_plus = ''
        if num == 13:
            for for_a in html_filters.list_by_kind('template'):
                top_plus += '' + \
                    '<a href="javascript:opennamu_forge_insert_v(\'data_field\', \'' + get_tool_js_safe(for_a.html) + '\')">' + html.escape(for_a.html) + '</a> : ' + html.escape(for_a.plus) + \
                    '<hr class="main_hr">' + \
                ''

        return await render_template(
            title_list[num][2],
            '''
                <form method="post">
                    ''' + top_plus + '''
                    <input class="__ON_INPUT__" placeholder="''' + placeholder + '''" id="data_field" name="name" type="text">
                    <hr class="main_hr">
                    <button class="__ON_BUTTON__" type="submit">''' + await get_lang('go') + '''</button>
                </form>
            ''',
            0,
            [['manager', await get_lang('return')]]
        )
