from .tool.func import *

# 개편 필요
async def login_find_email(tool):
    with get_db_connect() as conn:
        html_filters = get_html_filter_repository()
        user_settings = get_user_setting_repository()
        wiki_settings = get_wiki_settings_service()
        
        if flask.request.method == 'POST':
            re_set_list = ['c_id', 'c_pw', 'c_ans', 'c_que', 'c_key', 'c_type']
        
            if tool == 'email_change':
                flask.session['c_key'] = load_random_key(32)
                flask.session['c_id'] = ip_check()
                flask.session['c_type'] = 'email_change'
            elif tool == 'pass_find':
                user_id = flask.request.form.get('id', '')
                user_email = flask.request.form.get('email', '')
        
                flask.session['c_key'] = load_random_key(32)
                flask.session['c_id'] = user_id
                flask.session['c_type'] = 'pass_find'
            else:
                if not 'c_type' in flask.session:
                    return redirect(conn, '/register')
        
            if tool != 'pass_find':
                user_email = flask.request.form.get('email', '')
                email_data = re.search(r'@([^@]+)$', user_email)
                if email_data:
                    if not html_filters.exists(email_data.group(1), 'email'):
                        for i in re_set_list:
                            flask.session.pop(i, None)
                        
                        return redirect(conn, '/filter/email_filter')
                else:
                    for i in re_set_list:
                        flask.session.pop(i, None)
                    
                    return await re_error(conn, 36)
        
            email_title = wiki_settings.get(SettingKey.EMAIL_TITLE)
            t_text = html.escape(email_title) if email_title != '' else ((await wiki_set())[0] + ' key')
        
            email_text = wiki_settings.get(SettingKey.EMAIL_TEXT)
            i_text = (html.escape(email_text) + '\n\nKey : ' + flask.session['c_key']) if email_text != '' else ('Key : ' + flask.session['c_key'])
            
            if tool == 'pass_find':
                if not user_settings.exists_data(user_id, "email", user_email):
                    return await re_error(conn, 12)
                    
                if await send_email(conn, user_email, t_text, i_text) == 0:
                    return await re_error(conn, 18)
        
                return redirect(conn, '/pass_find/email')
            else:
                if user_settings.data_exists("email", user_email):
                    for i in re_set_list:
                        flask.session.pop(i, None)
        
                    return await re_error(conn, 35)
                
                if await send_email(conn, user_email, t_text, i_text) == 0:
                    for i in re_set_list:
                        flask.session.pop(i, None)
        
                    return await re_error(conn, 18)
        
                flask.session['c_email'] = user_email
        
                return redirect(conn, '/pass_find/email')
        else:
            if tool == 'pass_find':
                password_search_text = wiki_settings.get(SettingKey.PASSWORD_SEARCH_TEXT)
                b_text = (password_search_text + '<hr class="main_hr">') if password_search_text != '' else ''
        
                return await render_template(
                    await get_lang('password_search'),
                    b_text + '''
                        <form method="post">
                            <input class="__ON_INPUT__" placeholder="''' + await get_lang('id') + '''" name="id" type="text">
                            <hr class="main_hr">
                            <input class="__ON_INPUT__" placeholder="''' + await get_lang('email') + '''" name="email" type="text">
                            <hr class="main_hr">
                            <button class="__ON_BUTTON__" type="submit">''' + await get_lang('save') + '''</button>
                        </form>
                    ''',
                    '(' + await get_lang('email') + ')',
                    [['user', await get_lang('return')]]
                )
            else:
                if tool == 'need_email' and not 'c_type' in flask.session:
                    return redirect(conn, '/register')
        
                email_insert_text = wiki_settings.get(SettingKey.EMAIL_INSERT_TEXT)
                b_text = (email_insert_text + '<hr class="main_hr">') if email_insert_text != '' else ''
        
                return await render_template(
                    await get_lang('email'),
                    '''
                        <a href="/filter/email_filter">(''' + await get_lang('email_filter_list') + ''')</a>
                        <hr class="main_hr">
                        ''' + b_text + '''
                        <form method="post">
                            <input class="__ON_INPUT__" placeholder="''' + await get_lang('email') + '''" name="email" type="text">
                            <hr class="main_hr">
                            <button class="__ON_BUTTON__" type="submit">''' + await get_lang('save') + '''</button>
                        </form>
                    ''',
                    0,
                    [['user', await get_lang('return')]]
                )
