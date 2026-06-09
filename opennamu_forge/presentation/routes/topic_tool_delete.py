import flask

from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.dependencies import get_topic_repository
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    re_error,
    redirect,
    render_template,
)


async def topic_tool_delete(topic_num = 1):
    topics = get_topic_repository()

    if await acl_check(tool = 'owner_auth') == 1:
        return await re_error(3)

    topic_num = str(topic_num)

    if flask.request.method == 'POST':
        await acl_check(tool = 'owner_auth', memo = 'delete topic (' + topic_num + ')')

        topics.delete_thread(topic_num)

        return redirect('/')
    else:
        return await render_template(
            await get_lang('topic_delete'),
            '''
                <form method="post">
                    <span>''' + await get_lang('delete_warning') + '''</span>
                    <hr class="main_hr">
                    <button class="__ON_BUTTON__" type="submit">''' + await get_lang('delete') + '''</button>
                </form>
            ''',
            0,
            [['thread/' + topic_num + '/tool', await get_lang('return')]]
        )
