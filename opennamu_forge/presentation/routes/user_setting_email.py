import html

import flask

from opennamu_forge.application.dto.settings import SettingKey
from opennamu_forge.presentation.dependencies import (
    get_html_filter_repository,
    get_user_setting_repository,
    get_wiki_settings_service,
)
from opennamu_forge.presentation.email_helpers import send_email
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    re_error,
    redirect,
    render_template,
)
from opennamu_forge.presentation.shared.sql_dialect import ip_check, ip_or_user, re
from opennamu_forge.presentation.skin_helpers import wiki_set
from opennamu_forge.presentation.text_helpers import load_random_key


async def user_setting_email():
    html_filters = get_html_filter_repository()
    user_settings = get_user_setting_repository()
    wiki_settings = get_wiki_settings_service()

    ip = ip_check()
    if ip_or_user(ip) != 0:
        return redirect('/login')

    if flask.request.method == 'POST':
        # c_key 같은 이름 대신 한 기능에 고유 명칭 부여 필요
        re_set_list = ['c_key']
        flask.session['c_key'] = load_random_key(32)

        user_email = re.sub(r'\\', '', flask.request.form.get('email', ''))
        email_data = re.search(r'@([^@]+)$', user_email)
        if email_data:
            if not html_filters.exists(email_data.group(1), 'email'):
                for i in re_set_list:
                    flask.session.pop(i, None)

                return redirect('/filter/email_filter')
        else:
            for i in re_set_list:
                flask.session.pop(i, None)

            return await re_error(36)

        email_title = wiki_settings.get(SettingKey.EMAIL_TITLE)
        t_text = html.escape(email_title) if email_title != '' else ((await wiki_set())[0] + ' key')

        email_text = wiki_settings.get(SettingKey.EMAIL_TEXT)
        if email_text != '':
            i_text = html.escape(email_text) + '\n\nKey : ' + flask.session['c_key']
        else:
            i_text = 'Key : ' + flask.session['c_key']

        if user_settings.data_exists("email", user_email):
            for i in re_set_list:
                flask.session.pop(i, None)

            return await re_error(35)

        if await send_email(user_email, t_text, i_text) == 0:
            for i in re_set_list:
                flask.session.pop(i, None)

            return await re_error(18)

        flask.session['c_email'] = user_email

        return redirect('/change/email/check')
    else:
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
