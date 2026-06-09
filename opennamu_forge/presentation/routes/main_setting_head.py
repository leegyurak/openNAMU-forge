from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.shared.func import (
    flask,
    html,
    load_skin,
    re_error,
)
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    redirect,
    render_template,
)
from opennamu_forge.presentation.dependencies import get_other_setting_repository
async def main_setting_head(num, skin_name = '', set_preview = 0):
    if await acl_check('', 'owner_auth', '', '') == 1:
        return await re_error(0)

    other_settings = get_other_setting_repository()
    
    if flask.request.method == 'POST' and set_preview == 0:
        if num == 4:
            info_d = 'body'
            end_r = 'body/top'
            coverage = ''
        elif num == 7:
            info_d = 'bottom_body'
            end_r = 'body/bottom'
            coverage = ''
        else:
            info_d = 'head'
            end_r = 'head'
            if skin_name == '':
                coverage = ''
            else:
                coverage = skin_name

        other_settings.upsert(info_d, flask.request.form.get('content', ''), coverage=coverage)

        await acl_check(tool = 'owner_auth', memo = 'edit_set (' + info_d + ')')

        if skin_name == '':
            return redirect('/setting/' + end_r)
        else:
            return redirect('/setting/' + end_r + '/' + skin_name)
    else:
        title = ''
        start = ''
        form_action = ''
        data_preview = ''
        plus = ''
        data_name = 'head'
        coverage = skin_name

        if num == 4:
            title = '_body'
            form_action = 'formaction="/setting/body/top"'
            data_preview = flask.request.form.get('content', '') if set_preview == 1 else ''
            data_name = 'body'
            coverage = ''
            plus = '''
                <button class="__ON_BUTTON__" id="opennamu_forge_preview_button" type="submit" formaction="/setting_preview/body/top">''' + await get_lang('preview') + '''</button>
                <hr class="main_hr">
                <div id="opennamu_forge_preview_area">''' + data_preview + '''</div>
            '''
        elif num == 7:
            title = '_bottom_body'
            data_preview = flask.request.form.get('content', '') if set_preview == 1 else ''
            form_action = 'formaction="/setting/body/bottom"'
            data_name = 'bottom_body'
            coverage = ''
            plus = '''
                <button class="__ON_BUTTON__" id="opennamu_forge_preview_button" type="submit" formaction="/setting_preview/body/bottom">''' + await get_lang('preview') + '''</button>
                <hr class="main_hr">
                <div id="opennamu_forge_preview_area">''' + data_preview + '''</div>
            '''
        else:
            skin_list = ''
            for for_a in await load_skin('', 1):
                skin_list += '<a href="/setting/head/' + url_pas(for_a) + '">(' + html.escape(for_a) + ')</a> '
                skin_list += '<a href="/setting/head/' + url_pas(for_a) + '-cssdark">(' + html.escape(for_a) + '-cssdark)</a> '

            title = '_head'
            start = '' + \
                '<a href="/setting/head">(' + await get_lang('all') + ')</a> ' + \
                skin_list + '''
                <hr class="main_hr">
                <span>
                    &lt;style&gt;CSS&lt;/style&gt;
                    <br>
                    &lt;script&gt;JS&lt;/script&gt;
                </span>
                <hr class="main_hr">
            '''

        if set_preview == 1:
            data = data_preview
        else:
            data = other_settings.get(data_name, coverage=coverage)

        if skin_name != '':
            sub_plus = ' (' + skin_name + ')'
        else:
            sub_plus = ''

        return await render_template(
            await get_lang(data = 'main' + title, safe = 1),
            '''
                <form method="post">
                    ''' + start + '''
                    <textarea class="opennamu_forge_textarea_500 __ON_TEXTAREA__" placeholder="''' + await get_lang('enter_html') + '''" name="content" id="content">''' + html.escape(data) + '''</textarea>
                    <hr class="main_hr">
                    ''' + (await get_lang('main_css_warning') + '<hr class="main_hr">' if title == '_head' else '') + '''
                    <button class="__ON_BUTTON__" id="opennamu_forge_save_button" type="submit" ''' + form_action + '''>''' + await get_lang('save') + '''</button>
                    ''' + plus + '''
                </form>
            ''',
            '(HTML)' + sub_plus,
            [['setting', await get_lang('return')]]
        )
