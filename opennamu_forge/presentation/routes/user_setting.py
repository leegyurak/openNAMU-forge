from opennamu_forge.config.startup_options import get_init_set_list
from opennamu_forge.presentation.shared.func import (
    flask,
    get_user_title_list,
    html,
    ip_check,
    ip_or_user,
    load_skin,
    pw_encode,
)
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    http_warning,
    redirect,
    render_template,
)
from opennamu_forge.presentation.dependencies import get_user_setting_repository
async def user_setting():
    user_settings = get_user_setting_repository()

    support_language = ['default'] + get_init_set_list()['language']['list']
    
    ip = ip_check()

    if ip_or_user(ip) == 0:
        if flask.request.method == 'POST':
            auto_list = [
                ['skin', flask.request.form.get('skin', '')], 
                ['lang', flask.request.form.get('lang', '')],
                ['user_title', flask.request.form.get('user_title', '')],
                ['sub_user_name' , flask.request.form.get('sub_user_name', '')]
            ]
            if not auto_list[2][1] in await get_user_title_list(ip):
                auto_list[2][1] = ''

            twofa_on = flask.request.form.get('2fa', '')
            if twofa_on != '':
                twofa_pw = flask.request.form.get('2fa_pw', '')
                if twofa_pw != '':
                    twofa_pw = pw_encode(twofa_pw)

                    twofa_encode = user_settings.get(ip, 'encode')
                    
                    auto_list += [['2fa', 'on'], ['2fa_pw', twofa_pw], ['2fa_pw_encode', twofa_encode]]
                else:
                    auto_list += [['2fa', 'on']]
            else:
                auto_list += [['2fa', '']]

            for auto_data in auto_list:
                user_settings.upsert(ip, auto_data[0], auto_data[1])

            return redirect('/change')
        else:
            data = user_settings.get(ip, 'email')
            email = data if data != '' else '-'

            data = user_settings.get(ip, 'random_key')
            ramdom_key = data if data != '' else '-'

            div2 = await load_skin(user_settings.get(ip, 'skin'), 0, 1)

            data = user_settings.get(ip, 'lang', default='default')
            div3 = ''
            for lang_data in support_language:
                see_data = lang_data if lang_data != 'default' else await get_lang('default')

                if data == lang_data:
                    div3 = '<option value="' + lang_data + '">' + see_data + '</option>' + div3
                else:
                    div3 += '<option value="' + lang_data + '">' + see_data + '</option>'

            data = user_settings.get(ip, 'user_title')
            user_title_list = await get_user_title_list(ip)
            div4 = ''
            for user_title in user_title_list:                
                if data == user_title:
                    div4 = '<option value="' + user_title + '">' + user_title_list[user_title] + '</option>' + div4
                else:
                    div4 += '<option value="' + user_title + '">' + user_title_list[user_title] + '</option>'

            fa_data = user_settings.get(ip, '2fa')
            fa_data_select = ''
            fa_data_sp_list = [[await get_lang('off'), ''], [await get_lang('password'), 'on']]
            for fa_data_get in fa_data_sp_list:
                fa_data_selected = ''
                if fa_data == fa_data_get[1]:
                    fa_data_selected = 'selected'

                fa_data_select += '<option ' + fa_data_selected + ' value="' + fa_data_get[1] + '">' + fa_data_get[0] + '</option>'

            fa_data_pw = await get_lang('2fa_password_change') if user_settings.exists(ip, '2fa_pw') else await get_lang('2fa_password')

            db_data = user_settings.get(ip, 'user_name')
            user_name = db_data if db_data != '' else ip

            sub_user_name = user_settings.get(ip, 'sub_user_name')

            return await render_template(
                await get_lang('user_setting'),
                '''
                    <form method="post">
                        <div id="opennamu_forge_get_user_info">''' + html.escape(ip) + '''</div>
                        <hr class="main_hr">
                        <a href="/change/pw">(''' + await get_lang('password_change') + ''')</a>
                        <hr class="main_hr">
                        <span>''' + await get_lang('email') + ''' : ''' + email + '''</span> <a href="/change/email">(''' + await get_lang('email_change') + ''')</a> <a href="/change/email/delete">(''' + await get_lang('email_delete') + ''')</a>
                        <hr class="main_hr">
                        <span>''' + await get_lang('password_instead_key') + ''' : ''' + ramdom_key + ''' <a href="/change/key">(''' + await get_lang('key_change') + ''')</a> <a href="/change/key/delete">(''' + await get_lang('key_delete') + ''')</a></span>
                        <h2>''' + await get_lang('main') + '''</h2>
                        <a href="/change/head">(''' + await get_lang('user_head') + ''')</a> <a href="/change/top_menu">(''' + await get_lang('user_added_menu') + ''')</a>
                        <hr class="main_hr">
                        <span>''' + await get_lang('skin') + '''</span>
                        <hr class="main_hr">
                        <span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="skin">''' + div2 + '''</select></span>
                        <hr class="main_hr">
                        <a href="/change/skin_set">(''' + await get_lang('skin_set') + ''')</a> <a href="/change/skin_set/main">(''' + await get_lang('main_skin_set') + ''')</a>
                        <hr class="main_hr">
                        <span>''' + await get_lang('language') + '''</span>
                        <hr class="main_hr">
                        <span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="lang">''' + div3 + '''</select></span>
                        <hr class="main_hr">
                        <span>''' + await get_lang('user_title') + '''</span>
                        <hr class="main_hr">
                        <span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="user_title">''' + div4 + '''</select></span>
                        <h2>''' + await get_lang('2fa') + '''</h2>
                        <span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="2fa" id="twofa_check_input">''' + fa_data_select + '''</select></span>
                        <hr class="main_hr">
                        <input class="__ON_INPUT__" type="password" name="2fa_pw" placeholder="''' + fa_data_pw + '''">
                        <h2>''' + await get_lang('main_user_name') + '''</h2>
                        <a href="/change/user_name">(''' + await get_lang('change_user_name') + ''')</a>
                        <hr class="main_hr">
                        ''' + await get_lang('user_name') + ''' : ''' + html.escape(user_name) + '''
                        <h2>''' + await get_lang('sub_user_name') + '''</h2>
                        <input class="__ON_INPUT__" name="sub_user_name" value="''' + html.escape(sub_user_name) + '''" placeholder="''' + await get_lang('sub_user_name') + '''">
                        <hr class="main_hr">
                        <button class="__ON_BUTTON__" type="submit">''' + await get_lang('save') + '''</button>
                        ''' + await http_warning() + '''
                    </form>
                ''',
                0,
                [['user', await get_lang('return')]]
            )
    else:
        if flask.request.method == 'POST':
            flask.session['skin'] = flask.request.form.get('skin', '')
            flask.session['lang'] = flask.request.form.get('lang', '')

            return redirect('/change')
        else:
            div2 = await load_skin(
                ('' if not 'skin' in flask.session else flask.session['skin']), 
                0, 
                1
            )

            data = [['default']] if not 'lang' in flask.session else [[flask.session['lang']]]
            div3 = ''
            for lang_data in support_language:
                see_data = lang_data if lang_data != 'default' else await get_lang('default')

                if data and data[0][0] == lang_data:
                    div3 = '<option value="' + lang_data + '">' + see_data + '</option>' + div3
                else:
                    div3 += '<option value="' + lang_data + '">' + see_data + '</option>'

            return await render_template(
                await get_lang('user_setting'),
                '''
                    <form method="post">
                        <div id="opennamu_forge_get_user_info">''' + html.escape(ip) + '''</div>
                        <hr class="main_hr">
                        <h2>''' + await get_lang('main') + '''</h2>
                        <span>''' + await get_lang('skin') + '''</span>
                        <hr class="main_hr">
                        <span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="skin">''' + div2 + '''</select></span>
                        <hr class="main_hr">
                        <a href="/change/skin_set">(''' + await get_lang('skin_set') + ''')</a> <a href="/change/skin_set/main">(''' + await get_lang('main_skin_set') + ''')</a>
                        <hr class="main_hr">
                        <span>''' + await get_lang('language') + '''</span>
                        <hr class="main_hr">
                        <span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="lang">''' + div3 + '''</select></span>
                        <hr class="main_hr">
                        <button class="__ON_BUTTON__" type="submit">''' + await get_lang('save') + '''</button>
                        ''' + await http_warning() + '''
                        <hr class="main_hr">
                        <span>''' + await get_lang('user_head_warning') + '''</span>
                    </form>
                ''',
                0,
                [['user', await get_lang('return')]]
            )
