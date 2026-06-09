from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.shared.func import (
    flask,
    html,
    ip_check,
    ip_or_user,
)
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    redirect,
    render_template,
)
from opennamu_forge.presentation.dependencies import (
    get_history_repository,
    get_topic_repository,
    get_user_setting_repository,
)
def do_make_challenge_design(img, title, info, disable = 0):
    if disable == 1:
        table_style = 'style="border: 2px solid green"'
    else:
        table_style = 'style="border: 2px solid red"'
    
    return '''
        <table id="main_table_set" ''' + table_style + '''>
            <tr>
                <td id="main_table_width_quarter" rowspan="2">
                    <span style="font-size: 64px;">''' + img + '''</span>
                </td>
                <td>
                    <span style="font-size: 32px;">''' + title + '''</span>
                </td>
            </tr>
            <tr>
                <td>''' + info + '''</td>
        </table>
        <hr class="main_hr">
    '''

async def user_challenge():    
    histories = get_history_repository()
    topics = get_topic_repository()
    user_settings = get_user_setting_repository()
    
    ip = ip_check()
    if ip_or_user(ip) == 1:
        return redirect('/user')

    if flask.request.method == 'POST':
        user_exp = 0

        history_count = histories.count_by_ip(ip)
        user_exp += 5 * history_count

        if history_count >= 1:
            user_settings.upsert(ip, 'challenge_first_contribute', '1')
            user_exp += 500

        if history_count >= 10:
            user_settings.upsert(ip, 'challenge_tenth_contribute', '1')
            user_exp += 1000

        if history_count >= 100:
            user_settings.upsert(ip, 'challenge_hundredth_contribute', '1')
            user_exp += 3000        

        if history_count >= 1000:
            user_settings.upsert(ip, 'challenge_thousandth_contribute', '1')
            user_exp += 10000

        topic_count = topics.count_by_ip(ip)
        user_exp += 5 * topic_count

        if topic_count >= 1:
            user_settings.upsert(ip, 'challenge_first_discussion', '1')
            user_exp += 500    

        if topic_count >= 10:
            user_settings.upsert(ip, 'challenge_tenth_discussion', '1')
            user_exp += 1000

        if topic_count >= 100:
            user_settings.upsert(ip, 'challenge_hundredth_discussion', '1')
            user_exp += 3000

        if topic_count >= 1000:
            user_settings.upsert(ip, 'challenge_thousandth_discussion', '1')
            user_exp += 10000        

        if await acl_check(tool = 'all_admin_auth') != 1 or user_settings.exists(ip, 'challenge_admin'):
            user_settings.upsert(ip, 'challenge_admin', '1')
            user_exp += 10000

        exp = user_exp
        level = 0
        while 1:
            if exp >= (500 + level * 50):
                exp -= (500 + level * 50)
                level += 1
            else:
                break

        user_settings.upsert(ip, 'level', str(level))

        user_settings.upsert(ip, 'experience', str(exp))

        return redirect('/challenge')
    else:
        data_html_green = ''
        data_html_red = ''
        
        data_html_green += do_make_challenge_design(
            '🌳',
            await get_lang('challenge_title_register'), 
            await get_lang('challenge_info_register', 1),
            1
        )
        
        disable = 1 if user_settings.exists(ip, 'challenge_first_contribute') else 0
        data_html = do_make_challenge_design(
            '🔰',
            await get_lang('challenge_title_first_contribute'), 
            await get_lang('challenge_info_first_contribute', 1),
            disable
        )
        if disable == 1:
            data_html_green += data_html
        else:
            data_html_red += data_html
        
        disable = 1 if user_settings.exists(ip, 'challenge_tenth_contribute') else 0
        data_html = do_make_challenge_design(
            '📝',
            await get_lang('challenge_title_tenth_contribute'), 
            await get_lang('challenge_info_tenth_contribute', 1),
            disable
        )
        if disable == 1:
            data_html_green += data_html
        else:
            data_html_red += data_html
        
        disable = 1 if user_settings.exists(ip, 'challenge_hundredth_contribute') else 0
        data_html = do_make_challenge_design(
            '🖊️',
            await get_lang('challenge_title_hundredth_contribute'), 
            await get_lang('challenge_info_hundredth_contribute', 1),
            disable
        )
        if disable == 1:
            data_html_green += data_html
        else:
            data_html_red += data_html
        
        disable = 1 if user_settings.exists(ip, 'challenge_thousandth_contribute') else 0
        data_html = do_make_challenge_design(
            '🏅',
            await get_lang('challenge_title_thousandth_contribute'), 
            await get_lang('challenge_info_thousandth_contribute', 1),
            disable
        )
        if disable == 1:
            data_html_green += data_html
        else:
            data_html_red += data_html
        
        disable = 1 if user_settings.exists(ip, 'challenge_first_discussion') else 0
        data_html = do_make_challenge_design(
            '💬',
            await get_lang('challenge_title_first_discussion'), 
            await get_lang('challenge_info_first_discussion', 1),
            disable
        )
        if disable == 1:
            data_html_green += data_html
        else:
            data_html_red += data_html
        
        disable = 1 if user_settings.exists(ip, 'challenge_tenth_discussion') else 0
        data_html = do_make_challenge_design(
            '💡',
            await get_lang('challenge_title_tenth_discussion'), 
            await get_lang('challenge_info_tenth_discussion', 1),
            disable
        )
        if disable == 1:
            data_html_green += data_html
        else:
            data_html_red += data_html
        
        disable = 1 if user_settings.exists(ip, 'challenge_hundredth_discussion') else 0
        data_html = do_make_challenge_design(
            '📢',
            await get_lang('challenge_title_hundredth_discussion'), 
            await get_lang('challenge_info_hundredth_discussion', 1),
            disable
        )
        if disable == 1:
            data_html_green += data_html
        else:
            data_html_red += data_html
        
        disable = 1 if user_settings.exists(ip, 'challenge_thousandth_discussion') else 0
        data_html = do_make_challenge_design(
            '📜',
            await get_lang('challenge_title_thousandth_discussion'), 
            await get_lang('challenge_info_thousandth_discussion', 1),
            disable
        )
        if disable == 1:
            data_html_green += data_html
        else:
            data_html_red += data_html
            
        data_html = data_html_green + data_html_red

        disable = 1 if user_settings.exists(ip, 'challenge_admin') else 0
        data_html = do_make_challenge_design(
            '☑️',
            await get_lang('challenge_title_admin'), 
            await get_lang('challenge_info_admin', 1),
            disable
        )
        if disable == 1:
            data_html_green += data_html
        else:
            data_html_red += data_html
            
        data_html = data_html_green + data_html_red
        
        return await render_template(
            await get_lang('challenge_and_level_manage'),
            data_html + '''
                <form method="post">
                    <div id="opennamu_forge_get_user_info">''' + html.escape(ip) + '''</div>
                    <hr class="main_hr">
                    <button class="__ON_BUTTON__" id="opennamu_forge_save_button" type="submit">''' + await get_lang('reload') + '''</button>
                </form>
            ''',
            0,
            [['user', await get_lang('return')]]
        )
