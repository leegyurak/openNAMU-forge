from .tool.func import *

async def user_alarm():
    with get_db_connect() as conn:
        user_notices = get_user_notice_repository()
    
        num = int(number_check(flask.request.args.get('num', '1')))
        sql_num = (num * 50 - 50) if num * 50 > 0 else 0
    
        data = '<ul>'

        ip = ip_check()
    
        data_list = user_notices.list_by_user(ip, offset=sql_num, limit=50)
        if data_list:
            data = '' + \
                '<a href="/alarm/delete">(' + await get_lang('delete') + ')</a>' + \
                '<hr class="main_hr">' + \
                data + \
            ''
    
            for data_one in data_list:
                data_split = data_one.data.split(' | ')
                data_style = ''
                if data_one.read == '1':
                    data_style = 'opacity: 0.75;'
                
                data += '' + \
                    '<li style="' + data_style + '">' + \
                        await ip_pas(data_split[0]) + (' | ' + ' | '.join(data_split[1:]) if len(data_split) > 1 else '') + \
                        ' | ' + data_one.date + \
                        ' <a href="/alarm/delete/' + url_pas(data_one.notice_id) + '">(' + await get_lang('delete') + ')</a>' + \
                    '</li>' + \
                ''

        user_notices.mark_read(ip)
    
        data += '' + \
            '</ul>' + \
            await get_next_page_bottom('/alarm?num={}', num, data_list) + \
        ''
    
        return await render_template(
            await get_lang('notice'),
            data,
            0,
            [['user', await get_lang('return')]]
        )
