from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.shared.func import (
    get_next_page_bottom,
    html,
)
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    render_template,
)
from opennamu_forge.presentation.dependencies import (
    get_other_setting_repository,
    get_wiki_document_repository,
)
async def list_title_index(num = 1):
    sql_num = (num * 50 - 50) if num * 50 > 0 else 0
    other_settings = get_other_setting_repository()
    wiki_documents = get_wiki_document_repository()

    all_list = sql_num + 1
    data = ''

    title_list = wiki_documents.list_titles_page(offset=sql_num)
    if title_list:
        data += '<hr class="main_hr"><ul>'

    for list_data in title_list:
        data += '<li>' + str(all_list) + '. <a href="/w/' + url_pas(list_data) + '">' + html.escape(list_data) + '</a></li>'
        all_list += 1

    if num == 1:
        count_end = []

        all_title = other_settings.get("count_all_title", default="0")
        if int(all_title) < 30000:
            count_end += [int(all_title)]

            sql_list = ['category:', 'user:', 'file:']
            for sql in sql_list:
                count_end += [wiki_documents.count_titles(prefix=sql)]

            count_end += [count_end[0] - count_end[1]  - count_end[2]  - count_end[3]]

            data += '''
                </ul>
                <ul>
                    <li>''' + await get_lang('all') + ' : ' + str(count_end[0]) + '''</li>
                </ul>
                <ul>
                    <li>''' + await get_lang('category') + ' : ' + str(count_end[1]) + '''</li>
                    <li>''' + await get_lang('user_document') + ' : ' + str(count_end[2]) + '''</li>
                    <li>''' + await get_lang('file') + ' : ' + str(count_end[3]) + '''</li>
                    <li>''' + await get_lang('other') + ' : ' + str(count_end[4]) + '''</li>
            '''
        else:
            data += '''
                </ul>
                <ul>
                    <li>''' + await get_lang('all') + ' : ' + all_title + '''</li>
            '''

    data += '</ul>' + await get_next_page_bottom('/list/document/all/{}', num, title_list)
    sub = ' (' + str(num) + ')'

    return await render_template(
        await get_lang('all_document_list'),
        data,
        sub,
        [['other', await get_lang('return')]]
    )
