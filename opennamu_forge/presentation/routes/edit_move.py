from .tool.func import *

async def edit_move(name):
    with get_db_connect() as conn:
        wiki_documents = get_wiki_document_repository()
        document_meta = get_document_meta_repository()
        histories = get_history_repository()
        topics = get_topic_repository()

        if await acl_check(name, 'document_move') == 1:
            return await re_error(conn, 0)
        
        if do_title_length_check(conn, name) == 1:
            return await re_error(conn, 38)

        if flask.request.method == 'POST':
            move_title = flask.request.form.get('title', 'test')
            if await acl_check(move_title) == 1:
                return await re_error(conn, 0)

            if await captcha_post(conn, flask.request.form.get('g-recaptcha-response', flask.request.form.get('g-recaptcha', ''))) == 1:
                return await re_error(conn, 13)

            if await do_edit_slow_check(conn) == 1:
                return await re_error(conn, 24)
            
            send = flask.request.form.get('send', '')
            agree = flask.request.form.get('copyright_agreement', '')

            time = get_time()
            ip = ip_check()
            
            has_error = 0

            move_option = flask.request.form.get('move_option', 'none')
            move_option_topic = flask.request.form.get('move_topic_option', 'none')
            document_set_option = flask.request.form.get('document_set_option', 'none')
            
            if await do_edit_send_check(conn, send) == 1:
                return await re_error(conn, 37)
            
            if do_edit_text_bottom_check_box_check(conn, agree) == 1:
                return await re_error(conn, 29)

            # 역링크 관련 패치 해야할 듯

            # 문서 이동 파트 S
            if histories.exists_title(move_title):
                if move_option == 'merge' and await acl_check(tool = 'owner_auth', memo = 'merge documents (' + name + ') (' + move_title + ')') != 1:
                    if wiki_documents.exists_title(move_title):
                        wiki_documents.delete_title(move_title)
                        wiki_documents.delete_backlinks_by_link(move_title)

                    data_in = wiki_documents.get_data(name)

                    wiki_documents.rename_title(name, move_title)
                    wiki_documents.rename_backlink_link(name, move_title)

                    # 역링크 S
                    # 문서 합치기이므로 기존 문서 쪽은 no 역링크 생성, 이동하는 곳에는 no 역링크 제거
                    wiki_documents.insert_no_backlinks_for_title(name)
                    wiki_documents.delete_no_backlinks_for_title(move_title)
                    # 역링크 E

                    num = histories.latest_revision_id(move_title)
                    num = num if num else '0'

                    for move in histories.list_revision_ids_ascending(name):
                        new_revision_id = str(int(num) + int(move))
                        histories.rename_recent_change_title_and_id(name, move, move_title, new_revision_id)
                        histories.rename_revision_title_and_id(name, move, move_title, new_revision_id)

                    history_plus(conn, 
                        move_title, 
                        data_in, 
                        time, 
                        ip, 
                        send, 
                        '0',
                        t_check = '<a>' + name + '</a> ↔ <a>' + move_title + '</a>',
                        mode = 'move'
                    )
                elif move_option == 'reverse':
                    # 전체적인 구조 변경 필요
                    # 중간 문서 거치지 않고 불러와서 바로 변경하도록
                    # 문서 이동 말고 나머지도 그렇게 변경 필요함
                    i = 0
                    var_name = ''
                    while var_name == '':
                        temp_title = 'test ' + load_random_key() + ' ' + str(i)
                        if not histories.exists_title(temp_title):
                            var_name = temp_title
                        else:
                            i += 1

                    for title_name in [[name, var_name], [move_title, name], [var_name, move_title]]:
                        wiki_documents.rename_title(title_name[0], title_name[1])
                        wiki_documents.rename_backlink_link(title_name[0], title_name[1])

                        histories.rename_title(title_name[0], title_name[1])
                        histories.rename_recent_change_title(title_name[0], title_name[1])

                    for title_name in [[name, move_title], [move_title, name]]:
                        data_in = wiki_documents.get_data(name)

                        history_plus(conn, 
                            title_name[0], 
                            data_in, 
                            time, 
                            ip, 
                            send, 
                            '0',
                            t_check = '<a>' + title_name[0] + '</a> ⇋ <a>' + title_name[1] + '</a>',
                            mode = 'move'
                        )
                elif move_option != 'none':
                    has_error = 1
            elif move_option != 'none':
                data_in = wiki_documents.get_data(name)

                wiki_documents.rename_title(name, move_title)
                wiki_documents.rename_backlink_link(name, move_title)

                # 역링크 S
                # 문서 합치기 쪽 역링크와 동일하게
                wiki_documents.insert_no_backlinks_for_title(name)
                wiki_documents.delete_no_backlinks_for_title(move_title)
                # 역링크 E

                # 역사와 최근 변경 이동 S
                histories.rename_title(name, move_title)
                histories.rename_recent_change_title(name, move_title)
                # 역사와 최근 변경 이동 E

                history_plus(conn, 
                    move_title, 
                    data_in, 
                    time, 
                    ip, 
                    send,
                    '0',
                    t_check = '<a>' + name + '</a> → <a>' + move_title + '</a>',
                    mode = 'move'
                )

            # 문서 이동 파트 E
            
            # 토론 이동 파트 S
            if topics.exists_recent_discuss_title(move_title):
                if move_option_topic == 'merge' and await acl_check(tool = 'owner_auth', memo = 'merge document\'s topics (' + name + ') (' + move_title + ')') != 1:
                    topics.rename_recent_discuss_title(name, move_title)
                elif move_option_topic == 'reverse':
                    i = 0
                    var_name = ''
                    while var_name == '':
                        temp_title = 'test ' + load_random_key() + ' ' + str(i)
                        if not topics.exists_recent_discuss_title(temp_title):
                            var_name = temp_title
                        else:
                            i += 1
                    
                    for title_name in [[name, var_name], [move_title, name], [var_name, move_title]]:
                        topics.rename_recent_discuss_title(title_name[0], title_name[1])
                else:
                    has_error = 1
            elif move_option_topic != 'none':
                topics.rename_recent_discuss_title(name, move_title)

            # 토론 이동 파트 E

            # data_set 이동 파트 S
            if document_set_option == 'reverse':
                i = 0
                var_name = ''
                while var_name == '':
                    temp_title = 'test ' + load_random_key() + ' ' + str(i)
                    if not histories.exists_title(temp_title):
                        var_name = temp_title
                    else:
                        i += 1
                
                for title_name in [[name, var_name], [move_title, name], [var_name, move_title]]:
                    document_meta.rename_doc_name(title_name[0], title_name[1])
            elif document_set_option == 'normal':
                document_meta.delete_doc_name(move_title)
                document_meta.delete_acl_title(move_title)

                document_meta.rename_doc_name(name, move_title)
                document_meta.rename_acl_title(name, move_title)

            # data_set 이동 파트 E

            if has_error == 0:
                return redirect(conn, '/w/' + url_pas(move_title))
            else:
                return await re_error(conn, 19)
        else:
            owner_auth = await acl_check(tool = 'owner_auth')
            owner_auth = 1 if owner_auth == 0 else 0

            return await render_template(
                name,
                '''
                    <form method="post">
                        <span>''' + await get_lang('document_name') + '''</span>
                        <hr class="main_hr">
                        <input class="__ON_INPUT__" value="''' + name + '''" name="title" type="text">
                        <hr class="main_hr">
                        
                        <input class="__ON_INPUT__" placeholder="''' + await get_lang('why') + '''" name="send" type="text">
                        <hr class="main_hr">
                        
                        <h2>''' + await get_lang('document') + '''</h2>
                        <span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="move_option">
                            <option value="normal"> ''' + await get_lang('normal') + '''</option>
                            <option value="none"> ''' + await get_lang('dont_move') + '''</option>
                            <option value="reverse"> ''' + await get_lang('replace_move') + '''</option>
                            ''' + ('<option value="merge"> ' + await get_lang('merge_move') + '</option>' if owner_auth == 1 else '') + '''
                        </select></span>
                        <hr class="main_hr">
                        <!-- <label class="__ON_CHECKLABEL__"><input class="__ON_CHECKBOX__" type="checkbox" name="move_redirect_make"> ''' + await get_lang('move_redirect_make') + '''</label>
                        <hr class="main_hr"> -->
                        
                        <h2>''' + await get_lang('discussion') + '''</h2>
                        <span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="move_topic_option">
                            <option value="none"> ''' + await get_lang('dont_move') + '''</option>
                            <option value="normal"> ''' + await get_lang('normal') + '''</option>
                            <option value="reverse"> ''' + await get_lang('replace_move') + '''</option>
                            ''' + ('<option value="merge"> ' + await get_lang('merge_move') + '</option>' if owner_auth == 1 else '') + '''
                        </select></span>
                        <hr class="main_hr">

                        ''' + ((
                            '''<h2>''' + await get_lang('document_set') + '''</h2>
                            <span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="document_set_option">
                                <option value="none"> ''' + await get_lang('dont_move') + '''</option>
                                <option value="normal"> ''' + await get_lang('normal') + '''</option>
                                <option value="reverse"> ''' + await get_lang('replace_move') + '''</option>
                            </select></span>
                            <hr class="main_hr">
                            '''
                        ) if owner_auth == 1 else '') + '''

                        ''' + await captcha_get(conn) + await ip_warning(conn) + get_edit_text_bottom_check_box(conn) + get_edit_text_bottom(conn, 'move')  + '''
                        
                        <button class="__ON_BUTTON__" type="submit">''' + await get_lang('move') + '''</button>
                    </form>
                ''',
                '(' + await get_lang('move') + ')',
                [['w/' + url_pas(name), await get_lang('return')], ['move_all', await get_lang('multiple_move')]]
            )
