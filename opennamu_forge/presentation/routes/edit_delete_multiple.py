from opennamu_forge.presentation.captcha_helpers import captcha_get
from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.shared.func import (
    do_edit_send_check,
    do_edit_text_bottom_check_box_check,
    flask,
    get_edit_text_bottom,
    get_edit_text_bottom_check_box,
    ip_warning,
    re,
    re_error,
)
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    redirect,
    render_template,
)
from .edit_delete import edit_delete

async def edit_delete_multiple():
    if await acl_check('', 'acl_auth', '', '') == 1:
        return await re_error(0)

    if flask.request.method == 'POST':
        send = flask.request.form.get('send', '')
        agree = flask.request.form.get('copyright_agreement', '')
        
        if await do_edit_send_check(send) == 1:
            return await re_error(37)
        
        if do_edit_text_bottom_check_box_check(agree) == 1:
            return await re_error(29)
        
        all_title = re.findall(r'([^\n]+)\n', flask.request.form.get('content', '').replace('\r', '') + '\n')
        for name in all_title:
            await edit_delete(name)

        return redirect('/recent_change')
    else:
        return await render_template(
            await get_lang('many_delete'),
            '''
                <form method="post">
                    <textarea class="opennamu_forge_textarea_500 __ON_TEXTAREA__" placeholder="''' + await get_lang('many_delete_help') + '''" name="content"></textarea>
                    <hr class="main_hr">
                    <input class="__ON_INPUT__" placeholder="''' + await get_lang('why') + '''" name="send" type="text">
                    <hr class="main_hr">
                    ''' + await captcha_get() + await ip_warning() + get_edit_text_bottom_check_box() + get_edit_text_bottom('edit')  + '''
                    <button class="__ON_BUTTON__" type="submit">''' + await get_lang('delete') + '''</button>
                </form>
            ''',
            0,
            [['manager/1', await get_lang('return')]]
        )
