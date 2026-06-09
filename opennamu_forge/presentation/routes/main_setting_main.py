import html

import flask

from opennamu_forge.application.runtime_context import get_runtime_value
from opennamu_forge.config.startup_options import get_init_set_list
from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.dependencies import get_main_settings_form_service
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    re_error,
    redirect,
    render_simple_set,
    render_template,
)
from opennamu_forge.presentation.skin_helpers import load_skin


async def main_setting_main():
    if await acl_check('', 'owner_auth', '', '') == 1:
        return await re_error(0)

    main_settings = get_main_settings_form_service()

    if flask.request.method == 'POST':
        main_settings.update_from_form(flask.request.form.to_dict())

        await acl_check(tool = 'owner_auth', memo = 'edit_set (main)')

        return redirect('/setting/main')
    else:
        d_list = main_settings.load_form_values()

        init_set_list = get_init_set_list()
            
        # 언어도 변경 가능하도록 필요
            
        encode_select = ''
        encode_select_data = init_set_list['encode']['list'] + ['sha256']
        for encode_select_one in encode_select_data:
            if encode_select_one == d_list[15]:
                encode_select = '<option value="' + encode_select_one + '">' + encode_select_one + '</option>' + encode_select
            else:
                encode_select += '<option value="' + encode_select_one + '">' + encode_select_one + '</option>'
                
        tls_select = ''
        tls_select_data = ['http', 'https']
        for tls_select_one in tls_select_data:
            if tls_select_one == d_list[27]:
                tls_select = '<option value="' + tls_select_one + '">' + tls_select_one + '</option>' + tls_select
            else:
                tls_select += '<option value="' + tls_select_one + '">' + tls_select_one + '</option>'

        check_box_div = [7, 8, '', 20, 23, 24, '', 26, 31, 33, 34, 35, 36, 37, 44, 45, 47]
        for i in range(0, len(check_box_div)):
            acl_num = check_box_div[i]
            if isinstance(acl_num, int) and d_list[acl_num]:
                check_box_div[i] = 'checked="checked"'
            else:
                check_box_div[i] = ''

        set_data = get_runtime_value('db_type')
        
        sqlite_only = True
        if set_data != 'sqlite':
            sqlite_only = False

        ip_load_select_data = ''
        ip_load_option = ['default', 'HTTP_X_REAL_IP', 'HTTP_CF_CONNECTING_IP', 'REMOTE_ADDR']
        for for_a in ip_load_option:
            view_ip_option = for_a
            if for_a == 'default':
                view_ip_option = await get_lang('default')

            if d_list[46] == for_a:
                ip_load_select_data = '<option value="' + for_a + '">' + view_ip_option + '</option>' + ip_load_select_data
            else:
                ip_load_select_data += '<option value="' + for_a + '">' + view_ip_option + '</option>'

        basic_set = '''
            <h2>''' + await get_lang('basic_set') + '''</h2>
                        
            <span>''' + await get_lang('wiki_name') + '''</span>
            <hr class="main_hr">
            <input class="__ON_INPUT__" name="name" value="''' + html.escape(d_list[0]) + '''">
            <hr class="main_hr">

            <span><a href="/setting/main/logo">(''' + await get_lang('wiki_logo') + ''')</a></span>
            <hr class="main_hr">

            <span>''' + await get_lang('main_page') + '''</span>
            <hr class="main_hr">
            <input class="__ON_INPUT__" name="frontpage" value="''' + html.escape(d_list[2]) + '''">
            <hr class="main_hr">

            <span>''' + await get_lang('tls_method') + '''</span>
            <hr class="main_hr">
            <span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="http_select">''' + tls_select + '''</select></span>
            <hr class="main_hr">

            <span>''' + await get_lang('domain') + '''</span> (EX : 2du.pythonanywhere.com) (''' + await get_lang('off') + ''' : ''' + await get_lang('empty') + ''')
            <hr class="main_hr">
            <input class="__ON_INPUT__" name="domain" value="''' + html.escape(d_list[22]) + '''">
            <hr class="main_hr">

            <span>''' + await get_lang('wiki_host') + '''</span>
            <hr class="main_hr">
            <input class="__ON_INPUT__" name="host" value="''' + html.escape(d_list[16]) + '''">
            <hr class="main_hr">

            <span>''' + await get_lang('wiki_port') + '''</span>
            <hr class="main_hr">
            <input class="__ON_INPUT__" name="port" value="''' + html.escape(d_list[10]) + '''">
            <hr class="main_hr">

            <span>''' + await get_lang('wiki_secret_key') + '''</span>
            <hr class="main_hr">
            <input class="__ON_INPUT__" type="password" name="key" value="''' + html.escape(d_list[11]) + '''">
            <hr class="main_hr">
            
            <label class="__ON_CHECKLABEL__"><input class="__ON_CHECKBOX__" type="checkbox" name="wiki_access_password_need" ''' + check_box_div[8] + '''> ''' + await get_lang('set_wiki_access_password_need') + ''' (''' + await get_lang('restart_required') + ''')</label>
            <hr class="main_hr">
            
            <span>''' + await get_lang('set_wiki_access_password') + '''</span> (''' + await get_lang('restart_required') + ''')
            <hr class="main_hr">
            <input class="__ON_INPUT__" type="password" name="wiki_access_password" value="''' + html.escape(d_list[32]) + '''">
            <hr class="main_hr">

            <span>''' + await get_lang('wiki_load_ip_select') + '''</span> (''' + await get_lang('restart_required') + ''')
            <hr class="main_hr">
            <span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="load_ip_select">''' + ip_load_select_data + '''</select></span>
            
            <h3>''' + await get_lang('authority_use_list') + '''</h3>
            
            <label class="__ON_CHECKLABEL__"><input class="__ON_CHECKBOX__" type="checkbox" name="auth_history_off" ''' + check_box_div[14] + '''> ''' + await get_lang('authority_use_list_off') + '''</label>
            <hr class="main_hr">
            
            <span>''' + await get_lang('authority_use_list_expiration_date') + '''</span> (''' + await get_lang('day') + ''') (''' + await get_lang('off') + ''' : ''' + await get_lang('empty') + ''')
            <hr class="main_hr">
            <input class="__ON_INPUT__" name="auth_history_expiration_date" value="''' + html.escape(d_list[43]) + '''">
            <hr class="main_hr">

            <h3>''' + await get_lang('communication_set') + '''</h3>
            
            <label class="__ON_CHECKLABEL__"><input class="__ON_CHECKBOX__" type="checkbox" name="enable_comment" ''' + check_box_div[5] + '''> ''' + await get_lang('enable_comment_function') + '''</label>
            <hr class="main_hr">

            <label class="__ON_CHECKLABEL__"><input class="__ON_CHECKBOX__" type="checkbox" name="user_name_level" ''' + check_box_div[15] + '''> ''' + await get_lang('display_level_in_user_name') + '''</label>
            <hr class="main_hr">

            <label class="__ON_CHECKLABEL__"><input class="__ON_CHECKBOX__" type="checkbox" name="not_use_view_count" ''' + check_box_div[16] + '''> ''' + await get_lang('not_use_view_count') + '''</label>
            <hr class="main_hr">
        '''

        return await render_template(
            await get_lang('main_setting'),
            await render_simple_set('''
                <form method="post">
                    ''' + basic_set + '''
                    <h2>''' + await get_lang('design_set') + '''</h2>
                    
                    <span>''' + await get_lang('wiki_skin') + '''</span>
                    <hr class="main_hr">
                    <span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="skin">''' + await load_skin(d_list[5] if d_list[5] != '' else 'ringo') + '''</select></span>

                    <h2>''' + await get_lang('render_set') + '''</h2>
                    
                    <label class="__ON_CHECKLABEL__"><input class="__ON_CHECKBOX__" type="checkbox" name="namumark_compatible" ''' + check_box_div[10] + '''> ''' + await get_lang('namumark_fully_compatible_mode') + '''</label>
                    <hr class="main_hr">
                    
                    <label class="__ON_CHECKLABEL__"><input class="__ON_CHECKBOX__" type="checkbox" name="link_case_insensitive" ''' + check_box_div[12] + '''> ''' + await get_lang('link_case_insensitive') + '''</label>
                    <hr class="main_hr">

                    <h2>''' + await get_lang('login_set') + '''</h2>
                    
                    <label class="__ON_CHECKLABEL__"><input class="__ON_CHECKBOX__" type="checkbox" name="reg" ''' + check_box_div[0] + '''> ''' + await get_lang('no_register') + '''</label>
                    <hr class="main_hr">

                    <label class="__ON_CHECKLABEL__"><input class="__ON_CHECKBOX__" type="checkbox" name="ip_view" ''' + check_box_div[1] + '''> ''' + await get_lang('hide_ip') + '''</label>
                    <hr class="main_hr">

                    <label class="__ON_CHECKLABEL__"><input class="__ON_CHECKBOX__" type="checkbox" name="user_name_view" ''' + check_box_div[11] + '''> ''' + await get_lang('hide_user_name') + '''</label>
                    <hr class="main_hr">

                    <label class="__ON_CHECKLABEL__"><input class="__ON_CHECKBOX__" type="checkbox" name="requires_approval" ''' + check_box_div[3] + '''> ''' + await get_lang('requires_approval') + '''</label>
                    <hr class="main_hr">

                    <span>''' + await get_lang('password_min_length') + '''</span> (''' + await get_lang('off') + ''' : ''' + await get_lang('empty') + ''')
                    <hr class="main_hr">
                    <input class="__ON_INPUT__" name="password_min_length" value="''' + html.escape(d_list[30]) + '''">
                    <hr class="main_hr">

                    <span>''' + await get_lang('encryption_method') + '''</span>
                    <hr class="main_hr">
                    <span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="encode">''' + encode_select + '''</select></span>

                    <h3>''' + await get_lang('ua') + '''</h3>
                    
                    <label class="__ON_CHECKLABEL__"><input class="__ON_CHECKBOX__" type="checkbox" name="ua_get" ''' + check_box_div[4] + '''> ''' + await get_lang('ua_get_off') + '''</label>
                    <hr class="main_hr">
                    
                    <span>''' + await get_lang('ua_expiration_date') + '''</span> (''' + await get_lang('day') + ''') (''' + await get_lang('off') + ''' : ''' + await get_lang('empty') + ''')
                    <hr class="main_hr">
                    <input class="__ON_INPUT__" name="ua_expiration_date" value="''' + html.escape(d_list[42]) + '''">
                    <hr class="main_hr">
                    
                    <h2>''' + await get_lang('server_set') + '''</h2>

                    ''' + (
                    '''<h3>''' + await get_lang('backup') + ''' (''' + await get_lang('sqlite_only') + ''')</h3>
                    
                    <span>''' + await get_lang('backup_warning') + ''' (EX : data_YYYYMMDDHHMMSS.db)</span>
                    <hr class="main_hr">
                    <hr class="main_hr">
                    
                    <span>''' + await get_lang('backup_interval') + '''</span> (''' + await get_lang('hour') + ''') (''' + await get_lang('off') + ''' : ''' + await get_lang('empty') + ''')
                    <hr class="main_hr">
                    <input class="__ON_INPUT__" name="back_up" value="''' + html.escape(d_list[9]) + '''">
                    <hr class="main_hr">
                    
                    <span>''' + await get_lang('backup_where') + '''</span> (''' + await get_lang('default') + ''' : ''' + await get_lang('empty') + ''') (''' + await get_lang('example') + ''' : ./data/backup.db)
                    <hr class="main_hr">
                    <input class="__ON_INPUT__" name="backup_where" value="''' + html.escape(d_list[21]) + '''">
                    <hr class="main_hr">

                    <span>''' + await get_lang('backup_count') + '''</span> (''' + await get_lang('default') + ''' : ''' + await get_lang('empty') + ''')
                    <hr class="main_hr">
                    <input class="__ON_INPUT__" name="backup_count" value="''' + html.escape(d_list[41]) + '''">
                    <hr class="main_hr">''' if sqlite_only else ''
                    ) + '''

                    <h2>''' + await get_lang('edit_set') + '''</h2>
                    
                    <span>''' + await get_lang('slow_edit') + '''</span> (''' + await get_lang('second') + ''') (''' + await get_lang('off') + ''' : ''' + await get_lang('empty') + ''')
                    <hr class="main_hr">
                    <input class="__ON_INPUT__" name="slow_edit" value="''' + html.escape(d_list[19]) + '''">
                    <hr class="main_hr">
                    
                    <label class="__ON_CHECKLABEL__"><input class="__ON_CHECKBOX__" type="checkbox" name="edit_bottom_compulsion" ''' + check_box_div[7] + '''> ''' + await get_lang('edit_bottom_compulsion') + '''</label>
                    <hr class="main_hr">
                    
                    <span>''' + await get_lang('title_max_length') + '''</span> (''' + await get_lang('off') + ''' : ''' + await get_lang('empty') + ''')
                    <hr class="main_hr">
                    <input class="__ON_INPUT__" name="title_max_length" value="''' + html.escape(d_list[28]) + '''">
                    <hr class="main_hr">
                    
                    <span>''' + await get_lang('title_topic_max_length') + '''</span> (''' + await get_lang('off') + ''' : ''' + await get_lang('empty') + ''')
                    <hr class="main_hr">
                    <input class="__ON_INPUT__" name="title_topic_max_length" value="''' + html.escape(d_list[29]) + '''">
                    <hr class="main_hr">
                    
                    <span>''' + await get_lang('max_file_size') + ''' (MB)</span>
                    <hr class="main_hr">
                    <input class="__ON_INPUT__" name="upload" value="''' + html.escape(d_list[4]) + '''">
                    <hr class="main_hr">
                    
                    <label class="__ON_CHECKLABEL__"><input class="__ON_CHECKBOX__" type="checkbox" name="history_recording_off" ''' + check_box_div[9] + '''> ''' + await get_lang('set_history_recording_off') + '''</label>
                    <hr class="main_hr">

                    <label class="__ON_CHECKLABEL__"><input class="__ON_CHECKBOX__" type="checkbox" name="move_with_redirect" ''' + check_box_div[13] + '''> ''' + await get_lang('move_with_redirect') + ''' (''' + await get_lang('not_working') + ''')</label>
                    <hr class="main_hr">

                    <span>''' + await get_lang('slow_thread') + '''</span> (''' + await get_lang('second') + ''') (''' + await get_lang('off') + ''' : ''' + await get_lang('empty') + ''')
                    <hr class="main_hr">
                    <input class="__ON_INPUT__" name="slow_thread" value="''' + html.escape(d_list[38]) + '''">
                    <hr class="main_hr">

                    <span>''' + await get_lang('edit_timeout') + '''</span> (''' + await get_lang('second') + ''') (''' + await get_lang('off') + ''' : ''' + await get_lang('empty') + ''') (''' + await get_lang('linux_only') + ''')
                    <hr class="main_hr">
                    <input class="__ON_INPUT__" name="edit_timeout" value="''' + html.escape(d_list[39]) + '''">
                    <hr class="main_hr">

                    <span>''' + await get_lang('document_content_max_length') + '''</span> (''' + await get_lang('off') + ''' : ''' + await get_lang('empty') + ''')
                    <hr class="main_hr">
                    <input class="__ON_INPUT__" name="document_content_max_length" value="''' + html.escape(d_list[40]) + '''">
                    <hr class="main_hr">

                    <button class="__ON_BUTTON__" id="opennamu_forge_save_button" type="submit">''' + await get_lang('save') + '''</button>
                </form>
            '''),
            0,
            [['setting', await get_lang('return')]]
        )
