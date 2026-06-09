from .tool.func import *

async def user_count(name = None):
    with get_db_connect() as conn:
        histories = get_history_repository()
        topics = get_topic_repository()

        if name == None:
            that = ip_check()
        else:
            that = name

        data = histories.count_by_ip(that)

        data_topic = topics.count_by_ip(that)
            
        date = get_time()
        date = date.split()
        date = date[0]
        
        data_today = 0
        data_today_len = 0
            
        db_data = histories.list_lengths_by_ip_date_prefix(that, date)
        for count in db_data:
            count_data = count
            count_data = count_data.replace('+', '')
            count_data = count_data.replace('-', '')

            data_today_len += int(count_data)
            data_today += 1

        date_yesterday = str((
            datetime.datetime.today() + datetime.timedelta(days = -1)
        ).strftime("%Y-%m-%d"))
        
        data_yesterday = 0
        data_yesterday_len = 0
            
        db_data = histories.list_lengths_by_ip_date_prefix(that, date_yesterday)
        for count in db_data:
            count_data = count
            count_data = count_data.replace('+', '')
            count_data = count_data.replace('-', '')

            data_yesterday_len += int(count_data)
            data_yesterday += 1

        # 한글 지원 필요
        return await render_template(
            await get_lang('count'),
            '''
                <ul>
                    <li><a href="/record/''' + url_pas(that) + '''">''' + await get_lang('edit_record') + '''</a> : ''' + str(data) + '''</li>
                    <li><a href="/record/topic/''' + url_pas(that) + '''">''' + await get_lang('discussion_record') + '''</a> : ''' + str(data_topic) + '''</a></li>
                    <hr>
                    <li>(''' + await get_lang('beta') + ''') TODAY : ''' + str(data_today) + '''</li>
                    <li>(''' + await get_lang('beta') + ''') TODAY LEN : ''' + str(data_today_len) + '''</li>
                    <li>(''' + await get_lang('beta') + ''') TODAY DIFF : ''' + str(data_today_len - data_yesterday_len) + '''</li>
                    <hr>
                    <li>(''' + await get_lang('beta') + ''') YESTERDAY : ''' + str(data_yesterday) + '''</li>
                    <li>(''' + await get_lang('beta') + ''') YESTERDAY LEN : ''' + str(data_yesterday_len) + '''</li>
                </ul>
            ''',
            0,
            [['user', await get_lang('return')]]
        )
