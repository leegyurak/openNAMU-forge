import html

from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.dependencies import get_html_filter_repository
from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    re_error,
    render_template,
)


async def filter_all(tool):
    html_filters = get_html_filter_repository()

    div = '<table id="main_table_set">'
    div += '<tr id="main_table_top_tr">'

    div += '<td id="main_table_width">A</td>'
    div += '<td id="main_table_width">B</td>'
    div += '<td id="main_table_width">C</td>'

    div += '</tr>'

    admin = await acl_check(tool = 'owner_auth')
    admin = 1 if admin == 0 else 0

    if tool == 'edit_filter':
        if await acl_check('', 'edit_filter_view', '', '') == 1:
            return await re_error(0)

    if tool == 'inter_wiki':
        title = await get_lang('interwiki_list')
        filter_kind = 'inter_wiki'
    elif tool == 'email_filter':
        title = await get_lang('email_filter_list')
        filter_kind = 'email'
    elif tool == 'name_filter':
        title = await get_lang('id_filter_list')
        filter_kind = 'name'
    elif tool == 'edit_filter':
        title = await get_lang('edit_filter_list')
        filter_kind = 'regex_filter'
    elif tool == 'file_filter':
        title = await get_lang('file_filter_list')
        filter_kind = 'file'
    elif tool == 'image_license':
        title = await get_lang('image_license_list')
        filter_kind = 'image_license'
    elif tool == 'extension_filter':
        title = await get_lang('extension_filter_list')
        filter_kind = 'extension'
    elif tool == 'document':
        title = await get_lang('document_filter_list')
        filter_kind = 'document'
    elif tool == 'outer_link':
        title = await get_lang('outer_link_filter_list')
        filter_kind = 'outer_link'
    elif tool == 'template':
        title = await get_lang('template_document_list')
        filter_kind = 'template'
    else:
        title = await get_lang('edit_tool_list')
        filter_kind = 'edit_top'

    db_data = html_filters.list_by_kind(filter_kind)
    for data in db_data:
        div += '<tr>'
        div += '<td>'

        div += html.escape(data.html)
        if admin == 1:
            if tool in ('inter_wiki', 'outer_link', 'edit_filter', 'document', 'edit_top', 'template'):
                div += ' <a href="/filter/' + tool + '/add/' + url_pas(data.html) + '">(' + await get_lang('edit') + ')</a>'
                
            div += ' <a href="/filter/' + tool + '/del/' + url_pas(data.html) + '">(' + await get_lang('delete') + ')</a>'

        div += '</td>'

        if tool in ('inter_wiki', 'outer_link'):
            if tool == 'inter_wiki':
                div += '<td><a class="opennamu_forge_link_out" href="' + html.escape(data.plus) + '">' + html.escape(data.plus) + '</a></td>'
            else:
                div += '<td>' + html.escape(data.plus) + '</td>'
            
            div += '<td>' + data.plus_t + '</td>'
        else:
            div += '<td>' + html.escape(data.plus) + '</td>'
            div += '<td>' + html.escape(data.plus_t) + '</td>'
        
        div += '</tr>'

    div += '</table>'

    if admin == 1:
        div += '<hr class="main_hr">'
        div += '<a href="/filter/' + tool + '/add">(' + await get_lang('add') + ')</a>'

    return await render_template(
        title,
        div,
        0,
        [['manager/1', await get_lang('return')]]
    )
