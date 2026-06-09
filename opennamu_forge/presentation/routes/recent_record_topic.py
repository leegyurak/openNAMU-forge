import html

import flask

from opennamu_forge.presentation.dependencies import get_topic_repository
from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.identity_helpers import ip_pas
from opennamu_forge.presentation.pagination_helpers import get_next_page_bottom
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    render_template,
)
from opennamu_forge.presentation.text_helpers import number_check


async def recent_record_topic(name = 'Test'):
    topics = get_topic_repository()

    num = int(number_check(flask.request.args.get('num', '1')))
    sql_num = (num * 50 - 50) if num * 50 > 0 else 0

    div = '''
        <table id="main_table_set">
            <tr id="main_table_top_tr">
                <td id="main_table_width">''' + await get_lang('discussion_name') + '''</td>
                <td id="main_table_width">''' + await get_lang('writer') + '''</td>
                <td id="main_table_width">''' + await get_lang('time') + '''</td>
            </tr>
    '''
    sub = '(' + html.escape(name) + ')'
    pas_name = await ip_pas(name)

    data_list = topics.list_by_ip(name, offset=sql_num, limit=50)
    for data in data_list:
        title = html.escape(data.code)

        other_data = topics.get_recent_discuss(data.code)
        other_title = other_data.title if other_data is not None else ''
        other_subtitle = other_data.subtitle if other_data is not None else title

        div += '' + \
            '<tr>' + \
                '<td>' + \
                    '<a href="/thread/' + data.code + '#' + data.comment_id + '">' + other_subtitle + '#' + data.comment_id + '</a> (' + other_title + ')' + \
                '</td>' + \
                '<td>' + pas_name + '</td>' + \
                '<td>' + data.date + '</td>' + \
            '</tr>' + \
        ''

    div += '</table>'
    div += await get_next_page_bottom('/record/topic/' + url_pas(name) + '?num={}', num, data_list)

    return await render_template(
        await get_lang('discussion_record'),
        div,
        sub,
        [['other', await get_lang('other')], ['user/' + url_pas(name), await get_lang('user_tool')]]
    )
