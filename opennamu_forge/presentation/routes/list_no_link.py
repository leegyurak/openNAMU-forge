import html

from opennamu_forge.presentation.dependencies import get_document_meta_repository
from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.pagination_helpers import get_next_page_bottom
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    render_template,
)


async def list_no_link(num = 1):
    sql_num = (num * 50 - 50) if num * 50 > 0 else 0
    document_meta = get_document_meta_repository()
    
    div = '<ul>'
    
    n_list = document_meta.list_no_link_documents(offset=sql_num)
    for data in n_list:
        div += '<li>'
        div += data[1] + ' | <a href="/w/' + url_pas(data[0]) + '">' + html.escape(data[0]) + '</a>'
        
        db_data = document_meta.get(data[0], 'doc_type')
        if db_data != '':
            div += ' | ' + db_data

        div += '</li>'
    
    div += '</ul>' + await get_next_page_bottom('/list/document/no_link/{}', num, n_list)
    
    return await render_template(
        await get_lang('no_link_document_list'),
        div,
        0,
        [['other', await get_lang('return')]]
    )
