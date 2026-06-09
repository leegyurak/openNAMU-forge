from opennamu_forge.presentation.shared.func import (
    SettingKey,
    flask,
    ip_check,
    ip_or_user,
)
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    redirect,
    render_template,
)
from opennamu_forge.presentation.dependencies import (
    get_user_setting_repository,
    get_wiki_settings_service,
)
async def user_setting_email_check():
    user_settings = get_user_setting_repository()
    wiki_settings = get_wiki_settings_service()

    ip = ip_check()
    if ip_or_user(ip) != 0:
        return redirect('/login')

    re_set_list = ['c_key', 'c_email']
    if  not 'c_key' in flask.session or \
        not 'c_email' in flask.session:
        for i in re_set_list:
            flask.session.pop(i, None)

    if  flask.request.method == 'POST':
        ip = ip_check()
        input_key = flask.request.form.get('key', '')
        user_agent = flask.request.headers.get('User-Agent', '')

        if flask.session['c_key'] == input_key:
            user_settings.upsert(ip, "email", flask.session['c_email'])

        for i in re_set_list:
            flask.session.pop(i, None)

        return redirect('/change')
    else:
        check_key_text = wiki_settings.get(SettingKey.CHECK_KEY_TEXT)
        b_text = (check_key_text + '<hr class="main_hr">') if check_key_text != '' else ''

        return await render_template(
            await get_lang('check_key'),
            '''
                <form method="post">
                    ''' + b_text + '''
                    <input class="__ON_INPUT__" placeholder="''' + await get_lang('key') + '''" name="key" type="text">
                    <hr class="main_hr">
                    <button class="__ON_BUTTON__" type="submit">''' + await get_lang('save') + '''</button>
                </form>
            ''',
            0,
            [['user', await get_lang('return')]]
        )
