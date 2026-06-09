from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.shared.func import (
    flask,
    re_error,
)
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    redirect,
    render_template,
)
from opennamu_forge.presentation.dependencies import get_topic_repository
async def topic_comment_delete(topic_num = 1, num = 1):
    if await acl_check(tool = 'owner_auth') == 1:
        return await re_error(3)

    topic_num = str(topic_num)
    num = str(num)

    if flask.request.method == 'POST':
        get_topic_repository().delete(topic_num, num)

        return redirect('/thread/' + topic_num)
    else:
        return await render_template(
            await get_lang('topic_delete'),
            '''
                <hr class="main_hr">
                <form method="post">
                    <button class="__ON_BUTTON__" type="submit">''' + await get_lang('start') + '''</button>
                </form>
            ''',
            '(#' + num + ')',
            [['thread/' + topic_num + '/comment/' + num + '/tool', await get_lang('return')]]
        )
