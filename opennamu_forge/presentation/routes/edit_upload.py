from opennamu_forge.presentation.captcha_helpers import (
    captcha_get,
    captcha_post,
)
from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.file_helpers import load_image_url
from opennamu_forge.presentation.encoding_helpers import sha224_replace
from opennamu_forge.presentation.shared.func import (
    SettingKey,
    flask,
    get_time,
    history_plus,
    html,
    ip_check,
    os,
    re,
    re_error,
    render_set,
)
from opennamu_forge.presentation.text_helpers import (
    cache_v,
    number_check,
)
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    redirect,
    render_template,
)
from opennamu_forge.presentation.dependencies import (
    get_html_filter_repository,
    get_wiki_document_repository,
    get_wiki_settings_service,
)
async def edit_upload():
    html_filters = get_html_filter_repository()
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

        file_size_all = flask.request.content_length
        if file_size_all == None:
            file_size_all = 0

        if (file_max * 1000 * 1000 * file_len) < file_size_all or file_size_all == 0:
            return await re_error(17)

        if file_len == 1:
            file_num = None
        else:
            if await acl_check('', 'many_upload') == 1:
                return await re_error(0)

            file_num = 1

        for data in file_data:
            file_name = data.filename if data.filename else ''
            if file_name == '':
                return await re_error(9)
            
            value_tmp = os.path.splitext(file_name)
            value = ''
            if len(value_tmp) >= 2:
                value = value_tmp[1]

            extension = [i.html.lower() for i in html_filters.list_by_kind('extension')]
            if not re.sub(r'^\.', '', value).lower() in extension:
                return await re_error(14)

            name = ''
            if flask.request.form.get('f_name', None):
                name = flask.request.form.get('f_name', '') + (' ' + str(file_num) if file_num else '') + value
            else:
                name = file_name

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

            if wiki_settings.get(SettingKey.MARKUP) == 'namumark':
                file_d = '' + \
                    flask.request.form.get('f_lice_sel', 'direct_input') + '\n' + \
                    '[[category:' + re.sub(r'\]', '_', flask.request.form.get('f_lice_sel', '')) + ']]\n' + \
                    (g_lice if g_lice != '' else '') + \
                ''
            else:
                file_d = '' + \
                    flask.request.form.get('f_lice_sel', 'direct_input') + '\n' + \
                    (g_lice if g_lice != '' else '') + \
                ''

            wiki_documents.upsert_title('file:' + name, file_d)

            await render_set(
                doc_name = 'file:' + name,
                doc_data = file_d,
                data_type = 'backlink'
            )

            history_plus(
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
