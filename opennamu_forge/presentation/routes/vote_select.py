from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.shared.func import (
    flask,
    get_time,
    ip_check,
    re,
)
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    redirect,
    render_template,
)
from opennamu_forge.presentation.dependencies import get_vote_repository
async def vote_select(num = 1):
    votes = get_vote_repository()
    
    num = str(num)

    vote = votes.get_main(num)
    if vote is None:
        return redirect('/vote')

    if vote.type == 'close' or vote.type == 'n_close':
        return redirect('/vote/end/' + num)

    if await acl_check('', 'vote', num) == 1:
        return redirect('/vote/end/' + num)

    if votes.has_user_selection(num, ip_check()):
        return redirect('/vote/end/' + num)
    
    time_limit = votes.get_option(num, "end_date")
    if time_limit != '':
        
        time_db = time_limit.split()[0]
        time_today = get_time().split()[0]
        
        if time_today > time_db:
            return redirect('/vote/end/' + num)

    vote_data = re.findall(r'([^\n]+)', vote.data.replace('\r', ''))

    if flask.request.method == 'POST':
        try:
            vaild_check = int(flask.request.form.get('vote_data', '0'))
        except:
            return redirect('/vote/' + num)

        if len(vote_data) - 1 < vaild_check:
            return redirect('/vote/' + num)

        votes.add_selection(
            num,
            str(vaild_check),
            ip_check()
        )

        return redirect('/vote/end/' + num)
    else:
        data = '<h2>' + vote.name + '</h2>'
        data += '<b>' + vote.subject + '</b><hr class="main_hr">' if vote.subject != '' else ''
        data += '<span>~ ' + time_limit + '</span><hr class="main_hr">' if time_limit != '' else ''

        select_data = '<span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="vote_data">'
        line_num = 0
        for i in vote_data:
            select_data += '<option value="' + str(line_num) + '">' + i + '</option>'
            line_num += 1

        select_data += '</select></span>'
        data += '' + \
            '<form method="post">' + \
                select_data + \
                '<hr class="main_hr">' + \
                '<button class="__ON_BUTTON__" type="submit">' + await get_lang('send') + '</buttom>' + \
            '</form>' + \
        ''

        return await render_template(
            await get_lang('vote'),
            data,
            '(' + num + ')',
            [['vote', await get_lang('return')], ['vote/end/' + num, await get_lang('result')]]
        )
