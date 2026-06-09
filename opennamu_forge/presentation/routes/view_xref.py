from .tool.func import *

async def view_xref(name = 'Test', xref_type = 1, num = 1):
    with get_db_connect() as conn:
        backlinks = get_backlink_repository()
        document_meta = get_document_meta_repository()
        wiki_settings = get_wiki_settings_service()

        if await acl_check(name, 'render') == 1:
            return await re_error(conn, 0)

        sql_num = (num * 50 - 50) if num * 50 > 0 else 0

        if xref_type == 1:
            div = '<a href="/xref_this/' + url_pas(name) + '">(' + await get_lang('link_in_this') + ')</a><hr class="main_hr">'
            data_sub = '(' + await get_lang('backlink') + ')'
        else:
            div = '<a href="/xref/' + url_pas(name) + '">(' + await get_lang('normal') + ')</a><hr class="main_hr">'
            data_sub = '(' + await get_lang('link_in_this') + ')'

        div += '<ul>'

        if xref_type == 2:
            link_count = document_meta.get(name, 'link_count', default=await get_lang('data_missing'))
            div += '<li>' + await get_lang('link_count') + ' : ' +  link_count + '</li>'

        sql_insert = ['link', 'title'] if xref_type == 1 else ['title', 'link']
        if wiki_settings.get(SettingKey.LINK_CASE_INSENSITIVE) != '':
            data_list = backlinks.list_distinct_refs_case_insensitive(sql_insert[0], sql_insert[1], name, offset=sql_num)
        else:
            data_list = backlinks.list_distinct_refs(sql_insert[0], sql_insert[1], name, offset=sql_num)

        for data in data_list:
            div += '<li><a href="/w/' + url_pas(data[0]) + '">' + html.escape(data[0]) + '</a>'

            if data[1]:
                div += ' (' + data[1] + ')'

            if backlinks.has_include_title(data[0]):
                div += ' <a class="opennamu_forge_link_inter" href="/xref/' + url_pas(data[0]) + '">(' + await get_lang('backlink') + ')</a>'

            div += '</li>'

        div += '</ul>'
        
        if xref_type == 2:
            div += await get_next_page_bottom('/xref_this_page/{}/' + url_pas(name), num, data_list)
        else:
            div += await get_next_page_bottom('/xref_page/{}/' + url_pas(name), num, data_list)

        return await render_template(
            name,
            div,
            data_sub,
            [['w/' + url_pas(name), await get_lang('return')], ['xref_reset/' + url_pas(name), await get_lang('reset_backlink')]]
        )
