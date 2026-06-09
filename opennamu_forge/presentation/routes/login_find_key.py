from opennamu_forge.presentation.captcha_helpers import (
    captcha_get,
    captcha_post,
)
from opennamu_forge.presentation.shared.func import (
    SettingKey,
    flask,
    pw_encode,
    re_error,
)
from opennamu_forge.presentation.text_helpers import load_random_key
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    redirect,
    render_template,
)
from opennamu_forge.presentation.dependencies import (
    get_user_setting_repository,
    get_wiki_settings_service,
)
async def login_find_key():
    user_settings = get_user_setting_repository()
    wiki_settings = get_wiki_settings_service()
    if flask.request.method == 'POST':
        if await captcha_post(flask.request.form.get('g-recaptcha-response', flask.request.form.get('g-recaptcha', ''))) == 1:
            return await re_error(13)
        
        input_key = flask.request.form.get('key', '')
        user_id = user_settings.find_id_by_name_data("random_key", input_key)
        if user_id is None:
            return redirect('/user')
        
        key = load_random_key(32)
        user_settings.upsert(user_id, "pw", pw_encode(key))
        
        if user_settings.exists(user_id, "2fa"):
            user_settings.upsert(user_id, "2fa", "")
        
        reset_user_text = wiki_settings.get(SettingKey.RESET_USER_TEXT)
        b_text = (reset_user_text + '<hr class="main_hr">') if reset_user_text != '' else ''
        
        return await render_template(
                await get_lang('reset_user_ok'),
                '' + \
                    b_text + \
                    await get_lang('id') + ' : ' + user_id + \
                    '<hr class="main_hr">' + \
                    await get_lang('password') + ' : ' + key + \
                '',
                0,
                [['user', await get_lang('return')]]
        )
    else:
        return await render_template(
            await get_lang('password_search'),
            '''
                <form method="post">
                    <input class="__ON_INPUT__" placeholder="''' + await get_lang('key') + '''" name="key" type="password">
                    <hr class="main_hr">
                    ''' + await captcha_get() + '''
                    <button class="__ON_BUTTON__" type="submit">''' + await get_lang('send') + '''</button>
                </form>
            ''',
            0,
            [['user', await get_lang('return')]]
        )
