from opennamu_forge.presentation.captcha_helpers import (
    captcha_get,
    captcha_post,
)
from opennamu_forge.presentation.authorization_helpers import acl_check
import multiprocessing
import platform

from opennamu_forge.presentation.encoding_helpers import url_pas

from opennamu_forge.presentation.shared.func import (
    SettingKey,
    add_alarm,
    asyncio,
    do_edit_filter,
    do_edit_send_check,
    do_edit_slow_check,
    do_edit_text_bottom_check_box_check,
    do_title_length_check,
    edit_button,
    flask,
    get_edit_text_bottom,
    get_edit_text_bottom_check_box,
    get_main_skin_set,
    get_time,
    history_plus,
    html,
    ip_check,
    ip_warning,
    re,
    re_error,
    render_set,
)
from opennamu_forge.presentation.text_helpers import (
    leng_check,
    number_check,
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
    get_wiki_settings_service,
)
from .view_set import view_set_markup

async def edit_timeout(name, content, timeout = 3):
    try:
        await asyncio.wait_for(
            render_set(
                doc_name = name,
                doc_data = content
            ),
            timeout = timeout
        )

        return 0
    except asyncio.TimeoutError:
        return 1
        
async def edit_editor(ip, data_main = '', do_type = 'edit', addon = '', name = ''):
    document_meta = get_document_meta_repository()
    wiki_settings = get_wiki_settings_service()

    monaco_editor_top = ''
    div = ''

    if do_type == 'edit':
        help_text = wiki_settings.get(SettingKey.EDIT_HELP)

        div = document_meta.get(name, 'document_top')
    elif do_type == 'bbs':
        help_text = wiki_settings.get(SettingKey.BBS_HELP)
    elif do_type == 'bbs_comment':
        help_text = wiki_settings.get(SettingKey.BBS_COMMENT_HELP)
    else:
        help_text = wiki_settings.get(SettingKey.TOPIC_TEXT)

    if do_type == 'bbs_comment':
        do_type = 'thread'
    elif do_type == 'bbs':
        do_type = 'edit'
            
    p_text = html.escape(help_text) if help_text != '' else await get_lang('default_edit_help')
    
    monaco_editor_top += '<a href="javascript:opennamu_forge_do_editor_temp_save();">(' + await get_lang('load_temp_save') + ')</a> <a href="javascript:opennamu_forge_do_editor_temp_save_load();">(' + await get_lang('load_temp_save_load') + ')</a>'
    monaco_editor_top += '<hr class="main_hr">'
    
    darkmode = flask.request.cookies.get('main_css_darkmode', '0')
    monaco_thema = 'vs-dark' if darkmode == '1' else ''
    
    monaco_on = get_main_skin_set(flask.session, 'main_css_monaco', ip)
    editor_display = ['style="display: none;"' for _ in range(3)]
    if monaco_on == 'use':
        editor_display[1] = ''
    else:
        editor_display[0] = ''

    # 에디터 선택창
    monaco_editor_top += '<span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" onclick="do_sync_monaco_and_textarea();" id="opennamu_forge_select_editor" onchange="opennamu_forge_edit_turn_off_monaco();">'
    monaco_editor_top += '<option value="default" ' + ('selected' if editor_display[0] == '' else '') + '>' + await get_lang('default') + '</option>'
    monaco_editor_top += '<option value="monaco" ' + ('selected' if editor_display[1] == '' else '') + '>' + await get_lang('monaco_editor') + '</option>'
    monaco_editor_top += '</select></span> '

    # 문법 선택창
    if do_type == 'edit':
        monaco_editor_top += view_set_markup(document_name = name, addon = 'id="opennamu_forge_editor_markup" onclick="opennamu_forge_do_sync_monaco_markup();"')
    else:
        monaco_editor_top += view_set_markup(addon = 'id="opennamu_forge_editor_markup" onclick="opennamu_forge_do_sync_monaco_markup();"', disable = 'disabled')

    textarea_size = 'opennamu_forge_textarea_500' if do_type == 'edit' else 'opennamu_forge_textarea_100'

    out_field = await captcha_get() + await ip_warning() + addon
    if out_field != '':
        out_field += '<hr class="main_hr">'

    return '''
        <textarea class="__ON_TEXTAREA__" style="display: none;" id="opennamu_forge_edit_origin" name="doc_data_org">''' + html.escape(data_main) + '''</textarea>
        <div>
            ''' + monaco_editor_top + '''
            <hr class="main_hr">
            ''' + await edit_button() + '''
            <div id="opennamu_forge_editor_user_button"></div>
        </div>
        
        ''' + div + '''

        <div id="opennamu_forge_monaco_editor" class="''' + textarea_size + '''" ''' + editor_display[1] + '''></div>
        <textarea id="opennamu_forge_edit_textarea" class="''' + textarea_size + ''' __ON_TEXTAREA__" ''' + editor_display[0] + ''' name="content" placeholder="''' + p_text + '''">''' + html.escape(data_main) + '''</textarea>
        <hr class="main_hr">
        ''' + out_field + '''
        
        <script>
            window.addEventListener('DOMContentLoaded', function() {
                do_stop_exit();
                do_paste_image();
                do_monaco_init("''' + monaco_thema + '''");
                opennnamu_do_user_editor();
            });
        </script>
                        
        <button class="__ON_BUTTON__" id="opennamu_forge_save_button" type="submit" onclick="do_stop_exit_release();">''' + await get_lang('send') + '''</button>
        <button class="__ON_BUTTON__" id="opennamu_forge_preview_button" type="button" onclick="opennamu_forge_do_editor_preview();">''' + await get_lang('preview') + '''</button>
        <hr class="main_hr">

        <div id="opennamu_forge_preview_area"></div>
    '''

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
                if flask.request.form.get('doc_section_edit_apply', 'X') != 'X':
                    if flask.request.form.get('doc_section_data_where', '') != '':
                        data_match_where = flask.request.form.get('doc_section_data_where', '').split(',')
                        if len(data_match_where) == 2:
                            data_match_a = int(number_check(data_match_where[0]))
                            if data_match_where[1] != 'inf':
                                data_match_b = int(number_check(data_match_where[1]))
                            else:
                                data_match_b = 'inf'

                            try:
                                if data_match_b != 'inf':
                                    content = o_data[ : data_match_a] + content + o_data[data_match_b : ]
                                else:
                                    content = o_data[ : data_match_a] + content
                            except:
                                pass

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
                await add_alarm(scan_user, ip, '<a href="/w/' + url_pas(name) + '">' + html.escape(name) + '</a>')
                    
            history_plus(
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
                await add_alarm(scan_user, ip, '<a href="/edit_request/' + url_pas(name) + '">' + html.escape(name) + '</a> edit_request')
        
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
                if markup in ('namumark', 'namumark_beta'):
                    count = 1
                    data_section = '\n' + data + '\n'
                    
                    while 1:
                        data_match_re = r'\n((={1,6})(#?) ?([^\n]+)=)\n'
                        data_match = re.search(data_match_re, data_section)
                        if not data_match:
                            data_section = ''

                            break
                        elif count > section:
                            data_section = ''

                            break

                        if section == count:
                            data_section_sub = data_section
                            data_section_sub = re.sub(data_match_re, ('.' * (len(data_match.group(0)) - 1)) + '\n', data_section_sub, 1)

                            data_match_plus = re.search(data_match_re, data_section_sub)
                            if data_match_plus:
                                data_section = data[data_match.span()[0] : data_match_plus.span()[0] - 1]
                                data_section_where = str(data_match.span()[0]) + ',' + str(data_match_plus.span()[0] - 1)
                            else:
                                data_section = data[data_match.span()[0] : ]
                                data_section_where = str(data_match.span()[0]) + ',inf'

                            doc_section_edit_apply = 'O'

                            break
                        else:
                            data_section = re.sub(data_match_re, ('.' * (len(data_match.group(0)) - 1)) + '\n', data_section, 1)

                        count += 1
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
                    
                    ''' + await edit_editor(ip, data_section, addon = get_edit_text_bottom_check_box() + get_edit_text_bottom('edit') , name = name) + '''
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
