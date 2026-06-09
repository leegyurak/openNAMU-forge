from .tool.func import *

async def edit_delete(name):
    with get_db_connect() as conn:
        wiki_documents = get_wiki_document_repository()

        ip = ip_check()
        if await acl_check(name, 'document_delete') == 1:
            return await re_error(conn, 0)

        if not wiki_documents.exists_title(name):
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

            data = wiki_documents.get_data(name)
            today = get_time()
            leng = '-' + str(len(data))

            history_plus(conn, 
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

            return redirect(conn, '/w/' + url_pas(name))
        else:            
            return await render_template(
                name,
                '''
                    <form method="post">
                        <input class="__ON_INPUT__" placeholder="''' + await get_lang('why') + '''" name="send">
                        <hr class="main_hr">
                        ''' + await captcha_get(conn) + await ip_warning(conn) + get_edit_text_bottom_check_box(conn) + get_edit_text_bottom(conn, 'delete')  + '''
                        <button class="__ON_BUTTON__" type="submit">''' + await get_lang('delete') + '''</button>
                    </form>
                ''',
                '(' + await get_lang('delete') + ')',
                [['w/' + url_pas(name), await get_lang('return')]]
            )
