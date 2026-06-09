from .tool.func import *

async def edit_revert(name, num):
    with get_db_connect() as conn:
        history = get_history_repository()
        wiki_documents = get_wiki_document_repository()
        wiki_settings = get_wiki_settings_service()

        if history.is_hidden(name, str(num)) and await acl_check(tool = 'hidel_auth') == 1:
            return await re_error(conn, 3)

        if await acl_check(name, 'document_edit') == 1:
            return await re_error(conn, 0)
        
        data = history.find_data(name, str(num))
        if data is None:
            return redirect(conn, '/w/' + url_pas(name))

        if flask.request.method == 'POST':
            if await captcha_post(conn, flask.request.form.get('g-recaptcha-response', flask.request.form.get('g-recaptcha', ''))) == 1:
                return await re_error(conn, 13)

            if await do_edit_slow_check(conn) == 1:
                return await re_error(conn, 24)
            
            send = flask.request.form.get('send', '')
            agree = flask.request.form.get('copyright_agreement', '')
            
            if await do_edit_send_check(conn, send) == 1:
                return await re_error(conn, 37)
            
            if do_edit_text_bottom_check_box_check(conn, agree) == 1:
                return await re_error(conn, 29)

            if await do_edit_filter(conn, data) == 1:
                return await re_error(conn, 21)
            
            document_content_max_length = wiki_settings.get(SettingKey.DOCUMENT_CONTENT_MAX_LENGTH)
            if document_content_max_length != '':
                if int(number_check(document_content_max_length)) < len(data):
                    return await re_error(conn, 44)

            data_old = wiki_documents.get_data(name)
            if wiki_documents.exists_title(name):
                leng = leng_check(len(data_old), len(data))
            else:
                leng = '+' + str(len(data))

            wiki_documents.upsert_title(name, data)

            history_plus(conn, 
                name,
                data,
                get_time(),
                ip_check(),
                flask.request.form.get('send', ''),
                leng,
                t_check = 'r' + str(num),
                mode = 'revert'
            )

            await render_set(conn, 
                doc_name = name,
                doc_data = data,
                data_type = 'backlink'
            )

            return redirect(conn, '/w/' + url_pas(name))
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
                        ''' + await captcha_get(conn) + await ip_warning(conn) + get_edit_text_bottom_check_box(conn) + get_edit_text_bottom(conn, 'revert')  + '''
                        <button class="__ON_BUTTON__" type="submit">''' + await get_lang('revert') + '''</button>
                    </form>
                ''' + preview,
                '(r' + str(num) + ') (' + await get_lang('revert') + ')',
                [['history/' + url_pas(name), await get_lang('history')], ['recent_changes', await get_lang('recent_change')]]
            )
