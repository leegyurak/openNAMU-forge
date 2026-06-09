import html

import flask

from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.dependencies import (
    get_html_filter_repository,
    get_user_setting_repository,
)
from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    redirect,
    render_template,
)
from opennamu_forge.presentation.shared.sql_dialect import ip_check, re


async def user_edit_filter(name = ''):
    html_filters = get_html_filter_repository()
    user_settings = get_user_setting_repository()

    owner_auth = await acl_check(tool = 'ban_auth')
    owner_auth = 1 if owner_auth == 0 else 0

    if ip_check() != name:
        if owner_auth != 1:
            return redirect('/recent_block')

    if flask.request.method == 'POST':
        user_settings.delete(name, "edit_filter")

        return redirect('/edit_filter/' + url_pas(name))
    else:
        p_data = user_settings.get(name, "edit_filter")
        p_data = '<textarea readonly class="opennamu_forge_textarea_500 __ON_TEXTAREA__">' + html.escape(p_data) + '</textarea>'

        search_list = '<ul>'

        for data_list in html_filters.list_regex_filters_with_plus():
            match = re.compile(data_list.plus, re.I)
            search = match.search(p_data)
            if search:
                search = search.group()
                search_list += '<li>' + html.escape(search) + '</li>'

        search_list += '</ul>'
        search_list += '<hr class="main_hr">'

        delete = ''
        if owner_auth == 1:
            delete = '' + \
                '<form method="post">' + \
                    '<button class="__ON_BUTTON__" type="submit">' + await get_lang('delete') + '</button>' + \
                '</form>' + \
                '<hr class="main_hr">' + \
            ''

        return await render_template(
            name,
            '' + \
                '<a href="/filter/edit_filter">(' + await get_lang('edit_filter_rule') + ')</a>' + \
                '<hr class="main_hr">' + \
                p_data + search_list + delete + \
            '',
            '(' + await get_lang('edit_filter') + ')',
            [['recent_block', await get_lang('return')], ]
        )
