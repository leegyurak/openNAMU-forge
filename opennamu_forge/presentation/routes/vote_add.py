from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.shared.func import (
    flask,
    get_acl_list,
    ip_check,
    re,
    re_error,
)
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    redirect,
    render_template,
)
from opennamu_forge.presentation.dependencies import get_vote_repository
async def vote_add():
    votes = get_vote_repository()

    if await acl_check('', 'vote') == 1:
        return await re_error(0)

    if flask.request.method == 'POST':
        vote_data = flask.request.form.get('data', 'test\ntest_2')
        if vote_data.count('\n') < 1:
            return await re_error(0)

        latest_vote_id = votes.latest_vote_id()
        id_data = str((int(latest_vote_id) + 1) if latest_vote_id is not None else 1)

        if flask.request.form.get('open_select', 'N') == 'Y':
            open_data = 'open'
        else:
            open_data = 'n_open'

        votes.add_main(
            flask.request.form.get('name', 'test'),
            id_data,
            flask.request.form.get('subject', 'test'),
            flask.request.form.get('data', 'test'),
            open_data,
            flask.request.form.get('acl_select', '')
        )
        votes.add_option('open_user', id_data, ip_check())
        
        time_limitless = flask.request.form.get('limitless', '')
        if time_limitless == '':
            time_limit = flask.request.form.get('date', '')
            if re.search(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$', time_limit):
                votes.add_option('end_date', id_data, time_limit)

        return redirect('/vote')
    else:
        acl_data = '<span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="acl_select">'
        acl_list = await get_acl_list()
        for data_list in acl_list:
            acl_data += '<option value="' + data_list + '">' + (data_list if data_list != '' else 'normal') + '</option>'

        acl_data += '</select></span>'

        return await render_template(
            await get_lang('add_vote'),
            '' + \
                '<form method="post">' + \
                    '<input class="__ON_INPUT__" name="name" placeholder="' + await get_lang('name') + '">' + \
                    '<hr class="main_hr">' + \
                    '<textarea class="opennamu_forge_textarea_100 __ON_TEXTAREA__" name="subject" placeholder="' + await get_lang('explanation') + '"></textarea>' + \
                    '<hr class="main_hr">' + \
                    '<textarea class="opennamu_forge_textarea_500 __ON_TEXTAREA__" name="data" placeholder="' + await get_lang('1_line_1_q') + '"></textarea>' + \
                    '<hr class="main_hr">' + \
                    '<label class="__ON_CHECKLABEL__"><input class="__ON_CHECKBOX__" type="checkbox" value="Y" name="open_select"> ' + await get_lang('open_vote') + '</label>' + \
                    '<h2>' + await get_lang('period') + '</h2>'
                    '<input class="__ON_INPUT__" type="date" name="date" pattern="\\d{4}-\\d{2}-\\d{2}">' + \
                    '<hr class="main_hr">' + \
                    '<label class="__ON_CHECKLABEL__"><input class="__ON_CHECKBOX__" type="checkbox" value="Y" name="limitless"> ' + await get_lang('limitless') + '</label>' + \
                    '<h2>' + await get_lang('acl') + '</h2>' + \
                    acl_data + ' <a href="/acl/TEST#exp">(' + await get_lang('explanation') + ')</a>' + \
                    '<hr class="main_hr">' + \
                    '<button class="__ON_BUTTON__" type="submit">' + await get_lang('send') + '</buttom>' + \
                '</form>' + \
            '',
            0,
            [['vote', await get_lang('return')]]
        )
