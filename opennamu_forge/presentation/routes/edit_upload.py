import html
import os

import flask

from opennamu_forge.application.dto.settings import SettingKey
from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.captcha_helpers import (
    captcha_get,
    captcha_post,
)
from opennamu_forge.presentation.dependencies import (
    get_history_mutation_service,
    get_html_filter_repository,
    get_upload_policy_service,
    get_wiki_document_repository,
    get_wiki_settings_service,
)
from opennamu_forge.presentation.encoding_helpers import sha224_replace
from opennamu_forge.presentation.file_helpers import load_image_url
from opennamu_forge.presentation.rendering.render_helpers import render_set
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    re_error,
    redirect,
    render_template,
)
from opennamu_forge.presentation.shared.sql_dialect import get_time, ip_check, re
from opennamu_forge.presentation.text_helpers import (
    cache_v,
    number_check,
)


async def edit_upload():
    html_filters = get_html_filter_repository()
    upload_policy = get_upload_policy_service()
    wiki_documents = get_wiki_document_repository()
    wiki_settings = get_wiki_settings_service()

    if await acl_check('', 'upload') == 1:
        return await re_error(0)
    
    upload = wiki_settings.get(SettingKey.UPLOAD)
    file_max = number_check(upload) if upload != '' else '2'
    file_max = int(file_max)

    if flask.request.method == 'POST':
        if await captcha_post(flask.request.form.get('g-recaptcha-response', flask.request.form.get('g-recaptcha', ''))) == 1:
            return await re_error(13)

        file_data = flask.request.files.getlist("f_data[]")
        file_len = len(file_data)

        file_size_all = upload_policy.normalize_content_length(flask.request.content_length)

        if upload_policy.is_size_invalid(file_max, file_len, file_size_all):
            return await re_error(17)

        can_many_upload = True
        if file_len != 1:
            if await acl_check('', 'many_upload') == 1:
                can_many_upload = False

        file_num = upload_policy.initial_file_number(file_len, can_many_upload=can_many_upload)
        if file_num == 0:
            return await re_error(0)

        for data in file_data:
            file_name = data.filename if data.filename else ''
            if file_name == '':
                return await re_error(9)
            
            value_tmp = os.path.splitext(file_name)
            value = ''
            if len(value_tmp) >= 2:
                value = value_tmp[1]

            extension = [i.html.lower() for i in html_filters.list_by_kind('extension')]
            if re.sub(r'^\.', '', value).lower() not in extension:
                return await re_error(14)

            name = upload_policy.build_upload_title(file_name, flask.request.form.get('f_name', ''), file_num, value)

            piece = os.path.splitext(name)
            if re.search(r'\.', piece[0]):
                return await re_error(22)

            e_data = sha224_replace(piece[0]) + piece[1]

            if wiki_documents.exists_title('file:' + name):
                return await re_error(16)

            db_data = html_filters.list_by_kind('file')
            for i in db_data:
                t_re = re.compile(i.html)
                if t_re.search(name):
                    return redirect('/filter/file_filter')

            data_url_image = load_image_url()
            if os.path.exists(os.path.join(data_url_image, e_data)):
                return await re_error(16)
            else:
                data.save(os.path.join(data_url_image, e_data))

            ip = ip_check()
            g_lice = flask.request.form.get('f_lice', '')
            file_size = os.stat(os.path.join(data_url_image, e_data)).st_size
            file_size = str(round(file_size / 1000, 1))

            file_d = upload_policy.build_file_document_text(
                wiki_settings.get(SettingKey.MARKUP),
                flask.request.form.get('f_lice_sel', 'direct_input'),
                g_lice if g_lice != '' else '',
            )

            wiki_documents.upsert_title('file:' + name, file_d)

            await render_set(
                doc_name = 'file:' + name,
                doc_data = file_d,
                data_type = 'backlink'
            )

            get_history_mutation_service().add_history(
                'file:' + name,
                file_d,
                get_time(),
                ip,
                '',
                '0',
                mode = 'upload'
            )

            if file_num:
                file_num += 1

        return redirect('/w/file:' + name)
    else:
        license_list = '<option value="direct_input">' + await get_lang('direct_input') + '</option>'
        file_name = html.escape(flask.request.args.get('name', ''))

        db_data = html_filters.list_by_kind('image_license')
        license_list += ''.join(['<option value="' + i.html + '">' + i.html + '</option>' for i in db_data])

        upload_help_raw = wiki_settings.get(SettingKey.UPLOAD_HELP)
        upload_help = ('<hr class="main_hr">' + upload_help_raw) if upload_help_raw != '' else ''

        upload_default_raw = wiki_settings.get(SettingKey.UPLOAD_DEFAULT)
        upload_default = html.escape(upload_default_raw) if upload_default_raw != '' else ''
        
        return await render_template(
            await get_lang('upload'),
            '''
                <a href="/filter/file_filter">(''' + await get_lang('file_filter_list') + ''')</a> <a href="/filter/extension_filter">(''' + await get_lang('extension_filter_list') + ''')</a>
                ''' + upload_help + '''
                <hr class="main_hr">
                ''' + await get_lang('max_file_size') + ''' : ''' + str(file_max) + '''MB
                <hr class="main_hr">
                <form method="post" enctype="multipart/form-data" accept-charset="utf8">
                    <input class="__ON_INPUT__" multiple="multiple" type="file" name="f_data[]" id="file_input">
                    <hr class="main_hr">
                    <input class="__ON_INPUT__" placeholder="''' + await get_lang('file_name') + '''" name="f_name" value="''' + file_name + '''">
                    <hr class="main_hr">
                    <span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="f_lice_sel">
                        ''' + license_list + '''
                    </select></span>
                    <hr class="main_hr">
                    <textarea class="opennamu_forge_textarea_100 __ON_TEXTAREA__" placeholder="''' + await get_lang('other') + '''" name="f_lice">''' + upload_default + '''</textarea>
                    <hr class="main_hr">
                    ''' + await captcha_get() + '''
                    <button class="__ON_BUTTON__" id="opennamu_forge_save_button" type="submit">''' + await get_lang('save') + '''</button>
                </form>
                <hr class="main_hr">
                <div id="preview"></div>
                <script defer src="/views/main_css/js/func/file_preview.js''' + cache_v() + '''"></script>
                <script>window.addEventListener("DOMContentLoaded", function() { opennamu_forge_file_preview(); });</script>
            ''',
            0,
            [['other', await get_lang('return')]]
        )
