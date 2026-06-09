from opennamu_forge.presentation.shared.func import (
    SettingKey,
    add_user,
    flask,
)
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    redirect,
    render_template,
)
from opennamu_forge.presentation.dependencies import get_wiki_settings_service
async def login_register_email_check():
    wiki_settings = get_wiki_settings_service()

    if not 'reg_email' in flask.session:
        return redirect('/register')

    if  flask.request.method == 'POST':
        input_key = flask.request.form.get('key', '')

        if flask.session['reg_key'] != input_key:
            return redirect('/register')

        if wiki_settings.get(SettingKey.REQUIRES_APPROVAL) != '':
            flask.session['submit_id'] = flask.session['reg_id']
            flask.session['submit_pw'] = flask.session['reg_pw']
            flask.session['submit_email'] = flask.session['reg_email']

            return redirect('/register/submit')

        add_user(
            flask.session['reg_id'],
            flask.session['reg_pw'],
            flask.session['reg_email']
        )

        return redirect('/login')
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
