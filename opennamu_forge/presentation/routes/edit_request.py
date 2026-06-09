from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.shared.func import (
    add_alarm,
    flask,
    history_plus,
    html,
    render_set,
)
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    redirect,
    render_template,
)
from opennamu_forge.presentation.dependencies import (
    get_document_meta_repository,
    get_history_repository,
    get_user_setting_repository,
    get_wiki_document_repository,
)
from .view_diff import view_diff_do

async def edit_request(name = 'Test', do_type = ''):
    document_meta = get_document_meta_repository()
    history = get_history_repository()
    user_settings = get_user_setting_repository()
    wiki_documents = get_wiki_document_repository()

    disabled = ""
    if await acl_check(name, 'document_edit') == 1:
        disabled = "disabled"

    doc_ver = history.latest_revision_id(name) or '0'

    if doc_ver == '0':
        if await acl_check(name, 'document_make_acl') == 1:
            disabled = "disabled"

    if not document_meta.exists(name, 'edit_request_data', doc_rev=doc_ver):
        return redirect('/edit/' + url_pas(name))

    edit_request_data = document_meta.get(name, 'edit_request_data', doc_rev=doc_ver)

    edit_request_user = document_meta.get(name, 'edit_request_user', doc_rev=doc_ver)

    edit_request_date = document_meta.get(name, 'edit_request_date', doc_rev=doc_ver)

    edit_request_send = document_meta.get(name, 'edit_request_send', doc_rev=doc_ver)

    edit_request_leng = document_meta.get(name, 'edit_request_leng', doc_rev=doc_ver)

    if flask.request.method == 'POST':
        if disabled != "":
            return redirect('/w/' + url_pas(name))
        
        for scan_user in user_settings.list_ids_by_name_data('watchlist', name):
            await add_alarm(scan_user, edit_request_user, '<a href="/w/' + url_pas(name) + '">' + html.escape(name) + '</a>')

        if flask.request.form.get('check', '') == 'Y':
            wiki_documents.upsert_title(name, edit_request_data)
                    
            history_plus(
                name,
                edit_request_data,
                edit_request_date,
                edit_request_user,
                edit_request_send,
                edit_request_leng,
                mode = 'edit_request'
            )
            
            await render_set(
                doc_name = name,
                doc_data = edit_request_data,
                data_type = 'backlink'
            )
        else:
            history_plus(
                name,
                edit_request_data,
                edit_request_date,
                edit_request_user,
                edit_request_send,
                '0',
                mode = 'edit_request'
            )
            
        if do_type == 'from':
            return redirect('/edit/' + url_pas(name))
        else:
            return redirect('/w/' + url_pas(name))
    else:
        old_data = wiki_documents.get_data(name)

        result = view_diff_do(old_data, edit_request_data, 'r' + doc_ver, await get_lang('edit_request'))

        return await render_template(
            name,
            '''
                <div id="opennamu_forge_get_user_info">''' + html.escape(edit_request_user) + '''</div>
                <hr class="main_hr">
                ''' + edit_request_date + '''
                <hr class="main_hr">
                <input class="__ON_INPUT__" readonly value="''' + html.escape(edit_request_send) + '''">
                <hr class="main_hr">
                ''' + result + '''
                <hr class="main_hr">
                <form method="post">
                    <button class="__ON_BUTTON__" ''' + disabled + ''' id="opennamu_forge_save_button" type="submit" name="check" value="Y">''' + await get_lang('approve') + '''</button>
                    <button class="__ON_BUTTON__" ''' + disabled + ''' id="opennamu_forge_preview_button" type="submit" name="check" value="">''' + await get_lang('decline') + '''</button>
                    <hr class="main_hr">
                    <textarea readonly class="opennamu_forge_textarea_500 __ON_TEXTAREA__">''' + html.escape(edit_request_data) + '''</textarea>
                </form>
            ''',
            '(' + await get_lang('edit_request_check') + ')',
            0
        )
