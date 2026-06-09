import html

import flask

from opennamu_forge.application.dto.settings import SettingKey
from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.captcha_helpers import (
    captcha_get,
    captcha_post,
)
from opennamu_forge.presentation.dependencies import (
    get_history_mutation_service,
    get_history_repository,
    get_wiki_document_repository,
    get_wiki_settings_service,
)
from opennamu_forge.presentation.edit_toolbar_helpers import ip_warning
from opennamu_forge.presentation.edit_validation_helpers import (
    do_edit_filter,
    do_edit_send_check,
    do_edit_slow_check,
    do_edit_text_bottom_check_box_check,
    get_edit_text_bottom,
    get_edit_text_bottom_check_box,
)
from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.rendering.render_helpers import render_set
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    re_error,
    redirect,
    render_template,
)
from opennamu_forge.presentation.shared.sql_dialect import get_time, ip_check
from opennamu_forge.presentation.text_helpers import (
    leng_check,
    number_check,
)


async def edit_revert(name, num):
    history = get_history_repository()
    wiki_documents = get_wiki_document_repository()
    wiki_settings = get_wiki_settings_service()

    if history.is_hidden(name, str(num)) and await acl_check(tool = 'hidel_auth') == 1:
        return await re_error(3)

    if await acl_check(name, 'document_edit') == 1:
        return await re_error(0)
    
    data = history.find_data(name, str(num))
    if data is None:
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

        if await do_edit_filter(data) == 1:
            return await re_error(21)
        
        document_content_max_length = wiki_settings.get(SettingKey.DOCUMENT_CONTENT_MAX_LENGTH)
        if document_content_max_length != '':
            if int(number_check(document_content_max_length)) < len(data):
                return await re_error(44)

        data_old = wiki_documents.get_data(name)
        if wiki_documents.exists_title(name):
            leng = leng_check(len(data_old), len(data))
        else:
            leng = '+' + str(len(data))

        wiki_documents.upsert_title(name, data)

        get_history_mutation_service().add_history(
            name,
            data,
            get_time(),
            ip_check(),
            flask.request.form.get('send', ''),
            leng,
            t_check = 'r' + str(num),
            mode = 'revert'
        )

        await render_set(
            doc_name = name,
            doc_data = data,
            data_type = 'backlink'
        )

        return redirect('/w/' + url_pas(name))
    else:
        if data:
            preview = '<hr class="main_hr"><pre>' + html.escape(data) + '</pre>'
        else:
            preview = ''
        
        return await render_template(
            name,
            '''
                <form method="post">
                    <input class="__ON_INPUT__" placeholder="''' + await get_lang('why') + '''" name="send" type="text">
                    <hr class="main_hr">
                    ''' + await captcha_get() + await ip_warning() + get_edit_text_bottom_check_box() + get_edit_text_bottom('revert')  + '''
                    <button class="__ON_BUTTON__" type="submit">''' + await get_lang('revert') + '''</button>
                </form>
            ''' + preview,
            '(r' + str(num) + ') (' + await get_lang('revert') + ')',
            [['history/' + url_pas(name), await get_lang('history')], ['recent_changes', await get_lang('recent_change')]]
        )
