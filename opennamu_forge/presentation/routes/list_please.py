from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.shared.func import (
    get_next_page_bottom,
    html,
)
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    render_template,
)
from opennamu_forge.presentation.dependencies import get_wiki_document_repository
async def list_please(arg_num = 1):
    wiki_documents = get_wiki_document_repository()

    sql_num = (arg_num * 50 - 50) if arg_num * 50 > 0 else 0

    div = '<ul>'

    data_list = wiki_documents.list_needed_titles(offset=sql_num, limit=50)
    for data in data_list:
        div += '' + \
            '<li>' + \
                '<a class="opennamu_forge_not_exist_link" href="/w/' + url_pas(data) + '">' + html.escape(data) + '</a> ' + \
            '</li>' + \
        ''

    div += '</ul>' + await get_next_page_bottom('/list/document/need/{}', arg_num, data_list)

    return await render_template(
        await get_lang('need_document'),
        div,
        0,
        [['other', await get_lang('return')]]
    )
