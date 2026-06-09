from .tool.func import *

async def vote_end(num = 1):
    num = str(num)
    
    with get_db_connect() as conn:
        votes = get_vote_repository()

        vote = votes.get_main(num)
        if vote is None:
            return redirect(conn, '/vote')

        data = ''
        if vote.type == 'open' or vote.type == 'n_open':
            data += '<a href="/vote/close/' + num + '">(' + await get_lang('close_vote') + ')</a>'
        else:
            data += '<a href="/vote/close/' + num + '">(' + await get_lang('re_open_vote') + ')</a>'
        
        time_limit = votes.get_option(num, "end_date")

        data += '<h2>' + vote.name + '</h2>'
        data += '<b>' + vote.subject + '</b><hr class="main_hr">' if vote.subject != '' else ''
        data += '<span>~ ' + time_limit + '</span><hr class="main_hr">' if time_limit != '' else ''

        vote_data = re.findall(r'([^\n]+)', vote.data.replace('\r', ''))
        for i in range(0, len(vote_data)):
            data += '<h2>' + vote_data[i] + '</h2>'
            data += '<ul>'

            data_list_2 = votes.list_selection_users(num, str(i))
            if vote.type == 'open' or vote.type == 'close':
                all_ip = await ip_pas(data_list_2)
                for j in data_list_2:
                    data += '<li>' + all_ip[j] + '</li>'

            data += '<li>' + await get_lang('result') + ' : ' + str(len(data_list_2)) + '</li>'
            data += '</ul>'

        return await render_template(
            await get_lang('result_vote'),
            data,
            '(' + num + ')',
            [['vote', await get_lang('return')]]
        )
