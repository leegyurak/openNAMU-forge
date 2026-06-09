from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.shared.func import (
    do_add_thread,
    do_reload_recent_thread,
    flask,
    get_time,
    html,
    re_error,
)
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    redirect,
    render_template,
)
from opennamu_forge.presentation.dependencies import get_topic_repository
async def topic_tool_change(topic_num = 1):
    topics = get_topic_repository()

    if await acl_check(tool = 'owner_auth') == 1:
        return await re_error(3)

    time = get_time()
    topic_num = str(topic_num)

    rd_d = topics.get_recent_discuss(topic_num)
    if rd_d is None:
        return redirect('/')

    if flask.request.method == 'POST':
        await acl_check(tool = 'owner_auth', memo = 'move_topic (code ' + topic_num + ')')

        title_d = flask.request.form.get('title', 'test')
        sub_d = flask.request.form.get('sub', 'test')

        topics.update_recent_discuss_title_subtitle(topic_num, title_d, sub_d)

        do_add_thread(topic_num, await get_lang('topic_name_change') + ' : ' + rd_d.subtitle + ' (' + rd_d.title + ') → ' + sub_d + ' (' + title_d + ')', '1')
        do_reload_recent_thread(topic_num, time)

        return redirect('/thread/' + topic_num)
    else:
        return await render_template(
            await get_lang('topic_name_change'),
            '''
                <form method="post">
                    ''' + await get_lang('document_name') + '''
                    <hr class="main_hr">
                    <input class="__ON_INPUT__" value="''' + html.escape(rd_d.title) + '''" name="title" type="text">
                    <hr class="main_hr">
                    ''' + await get_lang('discussion_name') + '''
                    <hr class="main_hr">
                    <input class="__ON_INPUT__" value="''' + html.escape(rd_d.subtitle) + '''" name="sub" type="text">
                    <hr class="main_hr">
                    <button class="__ON_BUTTON__" type="submit">''' + await get_lang('save') + '''</button>
                </form>
            ''',
            0,
            [['thread/' + topic_num + '/tool', await get_lang('return')]]
        )
