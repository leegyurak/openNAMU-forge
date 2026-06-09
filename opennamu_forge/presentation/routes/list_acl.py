from .tool.func import *

async def list_acl(arg_num = 1):
    with get_db_connect() as conn:
        admin = get_admin_repository()
        document_meta = get_document_meta_repository()

        sql_num = (arg_num * 50 - 50) if arg_num * 50 > 0 else 0

        div = '<ul>'

        list_data = document_meta.list_acl_entries(offset=sql_num, limit=50)
        for data in list_data:
            latest_time = admin.latest_record_time(action_prefix='acl (' + data.title + ')')
            time_data = (latest_time + ' | ') if latest_time != '' else ''

            why = document_meta.get_acl(data.title, 'why')
            why_data = (' | ' + why) if why != '' else ''

            div += '' + \
                    '<li>' + \
                    time_data + \
                    '<a href="/acl/' + url_pas(data.title) + '">' + html.escape(data.title) + '</a>' + \
                    why_data + \
                '</li>' + \
            ''

        div += '</ul>'
        div += await get_next_page_bottom('/list/document/acl/{}', arg_num, list_data)

        return await render_template(
            await get_lang('acl_document_list'),
            div,
            0,
            [['other', await get_lang('return')]]
        )
