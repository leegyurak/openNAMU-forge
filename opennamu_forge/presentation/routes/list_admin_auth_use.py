from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.identity_helpers import ip_pas
from opennamu_forge.presentation.shared.func import (
    SettingKey,
    flask,
    get_next_page_bottom,
    html,
    ip_or_user,
)
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    redirect,
    render_template,
)
from opennamu_forge.presentation.dependencies import (
    get_admin_repository,
    get_wiki_settings_service,
)
async def list_admin_auth_use(arg_num = 1, arg_search = 'normal'):
    admin = get_admin_repository()
    wiki_settings = get_wiki_settings_service()

    sql_num = (arg_num * 50 - 50) if arg_num * 50 > 0 else 0

    if flask.request.method == 'POST':
        return redirect('/list/admin/auth_use_page/1/' + url_pas(flask.request.form.get('search', 'normal')))
    else:
        arg_search = 'normal' if arg_search == '' else arg_search
        action_prefix = '' if arg_search == 'normal' else arg_search

        list_data = '<ul>'

        get_list = admin.list_records(action_prefix=action_prefix, offset=sql_num, limit=50)
        for data in get_list:
            do_data = data.action

            if ip_or_user(data.actor) != 0:
                ip_view = wiki_settings.get(SettingKey.IP_VIEW)
                ip_view = '' if await acl_check(tool = 'ban_auth') != 1 else ip_view
                
                if ip_view != '':
                    do_data = do_data.split(' ')
                    do_data = do_data[0] if do_data[0] in ['ban'] else data.action

            list_data += '<li>' + await ip_pas(data.actor) + ' | ' + html.escape(do_data) + ' | ' + data.time + '</li>'

        list_data += '</ul>'
        list_data += await get_next_page_bottom('/list/admin/auth_use_page/{}/' + url_pas(arg_search), arg_num, get_list)

        arg_search = html.escape(arg_search) if arg_search != 'normal' else ''

        return await render_template(
            await get_lang('authority_use_list'),
            '''
                <form method="post">
                    <input class="opennamu_forge_width_200 __ON_INPUT__" name="search" placeholder="''' + await get_lang('start_with_search') + '''" value="''' + arg_search + '''">
                    <button class="__ON_BUTTON__" type="submit">''' + await get_lang('search') + '''</button>
                </form>
                <hr class="main_hr">
            ''' + list_data,
            0,
            [['other', await get_lang('return')]]
        )
