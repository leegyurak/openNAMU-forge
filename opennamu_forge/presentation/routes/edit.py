import html
import platform

import flask

from opennamu_forge.application.dto.settings import SettingKey
from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.captcha_helpers import captcha_post
from opennamu_forge.presentation.dependencies import (
    get_discussion_service,
    get_document_meta_repository,
    get_history_mutation_service,
    get_history_repository,
    get_user_setting_repository,
    get_wiki_document_repository,
    get_wiki_settings_service,
)
from opennamu_forge.presentation.edit_presenter import edit_editor as render_edit_editor
from opennamu_forge.presentation.edit_presenter import edit_timeout
from opennamu_forge.presentation.edit_section_helpers import (
    apply_section_edit_content,
    resolve_section_edit_data,
)
from opennamu_forge.presentation.edit_validation_helpers import (
    do_edit_filter,
    do_edit_send_check,
    do_edit_slow_check,
    do_edit_text_bottom_check_box_check,
    do_title_length_check,
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

from .view_set import view_set_markup


def build_editor_markup_selector(name='', do_type='edit'):
    markup_selector_addon = 'id="opennamu_forge_editor_markup" onclick="opennamu_forge_do_sync_monaco_markup();"'
    if do_type == 'edit':
        return view_set_markup(document_name=name, addon=markup_selector_addon)

    return view_set_markup(addon=markup_selector_addon, disable='disabled')


async def edit_editor(ip, data_main='', do_type='edit', addon='', name=''):
    return await render_edit_editor(
        ip,
        data_main,
        do_type,
        addon,
        name,
        markup_selector_html=build_editor_markup_selector(name, do_type),
    )


async def edit(name = 'Test', section = 0, do_type = ''):
    document_meta = get_document_meta_repository()
    history = get_history_repository()
    user_settings = get_user_setting_repository()
    wiki_documents = get_wiki_document_repository()
    wiki_settings = get_wiki_settings_service()

    ip = ip_check()

    edit_req_mode = 0
    if await acl_check(name, 'document_edit') == 1:
        edit_req_mode = 1
        if await acl_check(name, 'document_edit_request') == 1:
            return redirect('/raw_acl/' + url_pas(name))
        
    if do_title_length_check(name) == 1:
        return await re_error(38)
    
    doc_ver = history.latest_revision_id(name) or '0'

    if doc_ver == '0':
        if await acl_check(name, 'document_make_acl') == 1:
            edit_req_mode = 1

    if document_meta.exists(name, 'edit_request_data', doc_rev=doc_ver):
        return redirect('/edit_request_from/' + url_pas(name))
    
    section = '' if section == 0 else section
    post_ver = flask.request.form.get('ver', '')
    if flask.request.method == 'POST':
        edit_repeat = 'error' if post_ver != doc_ver else 'post'
    else:
        edit_repeat = 'get'
    
    if edit_repeat == 'post':
        if await captcha_post(flask.request.form.get('g-recaptcha-response', flask.request.form.get('g-recaptcha', ''))) == 1:
            return await re_error(13)

        if await do_edit_slow_check() == 1:
            return await re_error(24)

        today = get_time()
        content = flask.request.form.get('content', '').replace('\r', '')
        send = flask.request.form.get('send', '')
        agree = flask.request.form.get('copyright_agreement', '')
        
        if await do_edit_filter(content) == 1:
            return await re_error(21)
        
        if await do_edit_filter(send) == 1:
            return await re_error(21)

        if await do_edit_send_check(send) == 1:
            return await re_error(37)

        if do_edit_text_bottom_check_box_check(agree) == 1:
            return await re_error(29)
        
        if wiki_documents.exists_title(name):
            o_data = wiki_documents.get_data(name).replace('\r', '')

            if section != '':
                content = apply_section_edit_content(
                    original_content=o_data,
                    section_content=content,
                    section_where=flask.request.form.get('doc_section_data_where', ''),
                    section_apply=flask.request.form.get('doc_section_edit_apply', 'X'),
                )

            leng = leng_check(len(o_data), len(content))
        else:
            leng = '+' + str(len(content))

        document_content_max_length = wiki_settings.get(SettingKey.DOCUMENT_CONTENT_MAX_LENGTH)
        if document_content_max_length != '':
            if int(number_check(document_content_max_length)) < len(content):
                return await re_error(44)

        edit_timeout_value = wiki_settings.get(SettingKey.EDIT_TIMEOUT)
        edit_timeout_value = number_check(edit_timeout_value) if edit_timeout_value != '' else ''
        if edit_timeout_value != '' and platform.system() in ('Linux', 'Darwin'):
            timeout = await edit_timeout(name, content, int(edit_timeout_value))
        else:
            timeout = 0

        if timeout == 1:
            return await re_error(41)
        
        if edit_req_mode == 0:
            # 진짜 기록 부분
            wiki_documents.upsert_title(name, content)
    
            for scan_user in user_settings.list_ids_by_name_data('watchlist', name):
                await get_discussion_service().add_alarm(scan_user, ip, '<a href="/w/' + url_pas(name) + '">' + html.escape(name) + '</a>')
                    
            get_history_mutation_service().add_history(
                name,
                content,
                today,
                ip,
                send,
                leng
            )
            
            await render_set(
                doc_name = name,
                doc_data = content,
                data_type = 'backlink'
            )
            
            section = (('#edit_load_' + str(section)) if section != '' else '')
            return redirect('/w/' + url_pas(name) + section)
        else:
            document_meta.upsert(name, 'edit_request_data', content, doc_rev=doc_ver)
            document_meta.upsert(name, 'edit_request_user', ip, doc_rev=doc_ver)
            document_meta.upsert(name, 'edit_request_date', today, doc_rev=doc_ver)
            document_meta.upsert(name, 'edit_request_send', send, doc_rev=doc_ver)
            document_meta.upsert(name, 'edit_request_leng', leng, doc_rev=doc_ver)
            document_meta.upsert(name, 'edit_request_doing', today, doc_rev=doc_ver)

            for scan_user in user_settings.list_ids_by_name_data('watchlist', name):
                await get_discussion_service().add_alarm(scan_user, ip, '<a href="/edit_request/' + url_pas(name) + '">' + html.escape(name) + '</a> edit_request')
        
            return redirect('/edit_request_from/' + url_pas(name))
    else:
        editor_top_text = ''

        doc_section_edit_apply = 'X'
        data_section = ''
        data_section_where = ''

        if edit_repeat == 'get':
            if do_type == 'load':
                if flask.session and 'edit_load_document' in flask.session:
                    load_title = flask.session['edit_load_document']
                else:
                    load_title = 0
            else:
                load_title = 0
            
            if load_title == 0 and section == '':
                load_title = name
                editor_top_text += '<a href="/manager/15/' + url_pas(name) + '">(' + await get_lang('load') + ')</a> '
            elif section != '':
                load_title = name
                
            data = wiki_documents.get_data(load_title)
            data = data.replace('\r', '')

            if section != '':
                markup = wiki_settings.get(SettingKey.MARKUP, default='namumark')
                section_edit_data = resolve_section_edit_data(data, section, markup)
                data_section = section_edit_data.content
                data_section_where = section_edit_data.where
                doc_section_edit_apply = section_edit_data.apply
        else:
            data = flask.request.form.get('content', '')
            data = data.replace('\r', '')
            
            data_section_where = flask.request.form.get('doc_section_data_where', '')
            doc_section_edit_apply = flask.request.form.get('doc_section_edit_apply', '')

            doc_ver = flask.request.form.get('ver', '')

            warning_edit = await get_lang('exp_edit_conflict') + ' '

            if flask.request.form.get('ver', '0') == '0':
                warning_edit += '<a href="/raw/' + url_pas(name) + '">(r' + doc_ver + ')</a>'
            else:
                warning_edit += '' + \
                    '<a href="/diff/' + flask.request.form.get('ver', '1') + '/' + doc_ver + '/' + url_pas(name) + '">' + \
                        '(r' + doc_ver + ')' + \
                    '</a>' + \
                ''

            warning_edit += '<hr class="main_hr">'
            editor_top_text = warning_edit + editor_top_text

        if data_section == '':
            data_section = data

        editor_top_text += '<a href="/filter/edit_filter">(' + await get_lang('edit_filter_rule') + ')</a>'

        if editor_top_text != '':
            editor_top_text += '<hr class="main_hr">'

        sub_menu = ' (' + str(section) + ')' if section != '' else ''
        sub_title = '(' + await get_lang('edit_request') + ')' if edit_req_mode == 1 else '(' + await get_lang('edit') + ')'

        return await render_template(
            name,
            editor_top_text + '''
                <form method="post">
                    <textarea class="__ON_TEXTAREA__" style="display: none;" name="doc_section_data_where">''' + data_section_where + '''</textarea>
                    <input class="__ON_INPUT__" style="display: none;" name="doc_section_edit_apply" value="''' + doc_section_edit_apply + '''">

                    <input class="__ON_INPUT__" style="display: none;" id="opennamu_forge_editor_doc_name" value="''' + html.escape(name) + '''">
                    <input class="__ON_INPUT__" style="display: none;" name="ver" value="''' + doc_ver + '''">
                    
                    <input class="__ON_INPUT__" placeholder="''' + await get_lang('why') + '''" name="send">
                    <hr class="main_hr">
                    
                    ''' + await edit_editor(
                        ip,
                        data_section,
                        addon=get_edit_text_bottom_check_box() + get_edit_text_bottom('edit'),
                        name=name,
                    ) + '''
                </form>
            ''',
            sub_title + sub_menu,
            [
                ['w/' + url_pas(name), await get_lang('return')],
                ['delete/' + url_pas(name), await get_lang('delete')], 
                ['move/' + url_pas(name), await get_lang('move')], 
                ['upload', await get_lang('upload')]
            ]
        )
