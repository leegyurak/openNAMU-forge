import html

from opennamu_forge.presentation.dependencies import get_wiki_document_repository
from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.pagination_helpers import get_next_page_bottom
from opennamu_forge.presentation.rendering.render_helpers import render_set
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    render_template,
)


async def list_image_file(arg_num = 1, do_type = 0):
    sql_num = (arg_num * 50 - 50) if arg_num * 50 > 0 else 0
    wiki_documents = get_wiki_document_repository()

    list_data = ''
    if do_type == 0:
        list_data += '<a href="/list/image">(' + await get_lang('image') + ')</a>'
    else:
        list_data += '<a href="/list/file">(' + await get_lang('normal') + ')</a>'
    
    list_data += '<hr class="main_hr">'

    if do_type == 1:
        render_data = ''
        sub_data = ''
        count = 0

        data_list = wiki_documents.list_titles_page(offset=sql_num, prefix="file:")
        for data in data_list:
            if count != 0 and count % 4 == 0:
                render_data += '||\n'
                render_data += sub_data + '||\n'
                
                sub_data = ''

            render_data += '|| [[' + data + ']] '
            sub_data += '|| [[:' + data + ']] '
            count += 1

        if render_data != '':
            render_data += '||\n'
            render_data += sub_data + '||'

        end_data = await render_set(
            doc_name = '',
            doc_data = render_data,
            data_type = 'view',
            markup = 'namumark'
        )
        list_data += end_data
    else:
        list_data += '<ul>'

        data_list = wiki_documents.list_titles_page(offset=sql_num, prefix="file:")
        for data in data_list:
            list_data += '<li><a href="/w/' + url_pas(data) + '">' + html.escape(data) + '</a></li>'

        list_data += '</ul>'

    if do_type == 0:
        list_data += await get_next_page_bottom('/list/file/{}', arg_num, data_list)
    else:
        list_data += await get_next_page_bottom('/list/image/{}', arg_num, data_list)

    return await render_template(
        await get_lang('image_file_list'),
        list_data,
        0,
        [['other', await get_lang('return')]]
    )
