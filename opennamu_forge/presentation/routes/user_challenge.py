import flask

from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.challenge_presenter import render_challenge_body
from opennamu_forge.presentation.dependencies import (
    get_challenge_progress_service,
    get_user_setting_repository,
)
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    redirect,
    render_template,
)
from opennamu_forge.presentation.shared.sql_dialect import ip_check, ip_or_user


async def user_challenge():    
    challenge_progress = get_challenge_progress_service()
    user_settings = get_user_setting_repository()
    
    ip = ip_check()
    if ip_or_user(ip) == 1:
        return redirect('/user')

    if flask.request.method == 'POST':
        challenge_progress.refresh_user_progress(ip, await acl_check(tool = 'all_admin_auth'))

        return redirect('/challenge')
    else:
        return await render_template(
            await get_lang('challenge_and_level_manage'),
            await render_challenge_body(ip, user_settings, get_lang),
            0,
            [['user', await get_lang('return')]]
        )
