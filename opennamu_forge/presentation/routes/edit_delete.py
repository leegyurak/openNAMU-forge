import flask

from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.captcha_helpers import (
    captcha_get,
    captcha_post,
)
from opennamu_forge.presentation.dependencies import get_history_mutation_service, get_wiki_document_repository
from opennamu_forge.presentation.edit_toolbar_helpers import ip_warning
from opennamu_forge.presentation.edit_validation_helpers import (
    do_edit_send_check,
    do_edit_slow_check,
    do_edit_text_bottom_check_box_check,
    get_edit_text_bottom,
    get_edit_text_bottom_check_box,
)
from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    re_error,
    redirect,
    render_template,
)
from opennamu_forge.presentation.shared.sql_dialect import get_time, ip_check


async def edit_delete(name):
    wiki_documents = get_wiki_document_repository()

    ip = ip_check()
    if await acl_check(name, 'document_delete') == 1:
        return await re_error(0)

    if not wiki_documents.exists_title(name):
        return redirect('/w/' + url_pas(name))

    if flask.request.method == 'POST':
        if await captcha_post(flask.request.form.get('g-recaptcha-response', flask.request.form.get('g-recaptcha', ''))) == 1:
            return await re_error(13)

        if await do_edit_slow_check() == 1:
            return await re_error(24)
        
        send = flask.request.form.get('send', '')
        agree = flask.request.form.get('copyright_agreement', '')
        
        if await do_edit_send_check(send) == 1:
            return await re_error(37)
        
        if do_edit_text_bottom_check_box_check(agree) == 1:
            return await re_error(29)

        data = wiki_documents.get_data(name)
        today = get_time()
        leng = '-' + str(len(data))

        get_history_mutation_service().add_history(
            name,
            '',
            today,
            ip,
            send,
            leng,
            mode = 'delete'
        )

        wiki_documents.insert_no_backlinks_for_title(name)
        wiki_documents.delete_backlinks_by_link(name)
        wiki_documents.delete_title(name)

        return redirect('/w/' + url_pas(name))
    else:            
        return await render_template(
            name,
            '''
                <form method="post">
                    <input class="__ON_INPUT__" placeholder="''' + await get_lang('why') + '''" name="send">
                    <hr class="main_hr">
                    ''' + await captcha_get() + await ip_warning() + get_edit_text_bottom_check_box() + get_edit_text_bottom('delete')  + '''
                    <button class="__ON_BUTTON__" type="submit">''' + await get_lang('delete') + '''</button>
                </form>
            ''',
            '(' + await get_lang('delete') + ')',
            [['w/' + url_pas(name), await get_lang('return')]]
        )
