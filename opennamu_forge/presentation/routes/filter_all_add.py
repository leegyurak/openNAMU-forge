from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.shared.func import (
    flask,
    get_acl_list,
    html,
    re,
    re_error,
)
from opennamu_forge.presentation.text_helpers import number_check
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    redirect,
    render_template,
)
from opennamu_forge.presentation.dependencies import get_html_filter_repository
async def filter_all_add(tool, name = None):
    html_filters = get_html_filter_repository()

    if not name and tool == 'edit_filter':
        return redirect('/manager/9')

    if flask.request.method == 'POST':
        if await acl_check('', 'owner_auth', '', '') == 1:
            return await re_error(3)

        title = flask.request.form.get('title', 'test')
        if tool in ('inter_wiki', 'outer_link'):
            link = flask.request.form.get('link', 'test')
            icon = flask.request.form.get('icon', '')
            inter_type = flask.request.form.get('inter_type', '')

            html_filters.upsert(title, tool, plus=link, plus_t=icon)
            if tool == 'inter_wiki':
                html_filters.upsert(title, 'inter_wiki_sub', plus='inter_wiki_type', plus_t=inter_type)
            
            await acl_check(tool = 'owner_auth', memo = tool + ' edit')
        elif tool == 'edit_filter':
            day = flask.request.form.get('day', '0')
            end = 'X' if day == '0' else day
            if end != 'X':
                end = re.sub(r'[^0-9]', '', end)
                end = str(int(number_check(end)) * 24 * 60 * 60)

            content = flask.request.form.get('content', 'test')
            try:
                re.compile(content)
            except:
                return await re_error(23)
            
            html_filters.upsert(name, 'regex_filter', plus=content, plus_t=end)
            await acl_check(tool = 'owner_auth', memo = 'edit_filter edit')
        elif tool == 'document':
            post_name = flask.request.form.get('name', '')
            if post_name == '':
                return redirect('/filter/document')
        
            post_acl = flask.request.form.get('acl', '')
            post_regex = flask.request.form.get('regex', '')
            try:
                re.compile(post_regex)
            except:
                return await re_error(23)
            
            html_filters.upsert(post_name, 'document', plus=post_regex, plus_t=post_acl)
            await acl_check(tool = 'owner_auth', memo = 'document_filter edit')
        else:
            plus_d = ''
            if tool == 'name_filter':
                try:
                    re.compile(title)
                except:
                    return await re_error(23)

                await acl_check(tool = 'owner_auth', memo = 'name_filter edit')
                type_d = 'name'
            elif tool == 'file_filter':
                try:
                    re.compile(title)
                except:
                    return await re_error(23)

                await acl_check(tool = 'owner_auth', memo = 'file_filter edit')
                type_d = 'file'
            elif tool == 'email_filter':
                await acl_check(tool = 'owner_auth', memo = 'email_filter edit')
                type_d = 'email'
            elif tool == 'image_license':
                await acl_check(tool = 'owner_auth', memo = 'image_license edit')
                type_d = 'image_license'
            elif tool == 'extension_filter':
                await acl_check(tool = 'owner_auth', memo = 'extension_filter edit')
                type_d = 'extension'
                plus_d = flask.request.form.get('max_file_size', '')
                if plus_d != '':
                    plus_d = number_check(plus_d)
            elif tool == 'template':
                await acl_check(tool = 'owner_auth', memo = 'template_document edit')
                type_d = 'template'
                plus_d = flask.request.form.get('exp', 'test')
            else:
                await acl_check(tool = 'owner_auth', memo = 'edit_top edit')
                type_d = 'edit_top'
                plus_d = flask.request.form.get('markup', 'test')

            if name:
                html_filters.delete(name, type_d)

            html_filters.upsert(title, type_d, plus=plus_d)

        return redirect('/filter/' + tool)
    else:
        get_sub = 0
        stat = 'disabled' if await acl_check('', 'owner_auth', '', '') == 1 else ''
        name = name if name else ''

        if tool in ('inter_wiki', 'outer_link'):
            value = ['', '', '']
            if name != '':
                exist = html_filters.get(name, tool)
                value = [exist.html, exist.plus, exist.plus_t] if exist else value

            select = ''
            if tool == 'inter_wiki':
                ex = 'https://namu.wiki/w/'

                select = ['', '']
                if html_filters.get_plus_t(name, 'inter_wiki_sub') == 'under_bar':
                    select = ['', 'selected']

                select = '''
                    <hr class="main_hr">
                    ''' + await get_lang('inter_wiki_space_change') + '''
                    <hr class="main_hr">
                    <span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="inter_type">
                        <option ''' + select[0] + ''' value="url_encode">%20</option>
                        <option ''' + select[1] + ''' value="under_bar">_</option>
                    </select></span>
                '''
            else:
                ex = 'youtube.com'

            title = await get_lang('interwiki_add') if tool == 'inter_wiki' else await get_lang('outer_link_add')
            form_data = '''
                ''' + await get_lang('name') + '''
                <hr class="main_hr">
                <input class="__ON_INPUT__" value="''' + html.escape(value[0]) + '''" type="text" name="title">
                <hr class="main_hr">
                ''' + await get_lang('link') + ''' (EX : ''' + ex + ''')
                <hr class="main_hr">
                <input class="__ON_INPUT__" value="''' + html.escape(value[1]) + '''" type="text" name="link">
                <hr class="main_hr">
                ''' + await get_lang('icon') + ''' (''' + ('HTML' if tool == 'inter_wiki' else await get_lang('html_or_link')) + ''') (''' + await get_lang('link') + ' - EX' + ''' : /image/Test.svg)
                <hr class="main_hr">
                <input class="__ON_INPUT__" value="''' + html.escape(value[2]) + '''" type="text" name="icon">
                ''' + select + '''
            '''
        elif tool == 'edit_filter':            
            exist = html_filters.get(name, 'regex_filter')
            if exist:
                textarea = exist.plus
                time_data = '' if exist.plus_t == 'X' else exist.plus_t
                if time_data != '':
                    time_data = re.sub(r'[^0-9]', '', time_data)
                    time_data = str(int(int(number_check(time_data)) / (24 * 60 * 60)))
            else:
                textarea = ''
                time_data = ''

            title = await get_lang('edit_filter_add')
            form_data = '''
                <hr class="main_hr">
                <input class="__ON_INPUT__" placeholder="''' + await get_lang('day') + '''" name="day" type="text" value="''' + html.escape(time_data) + '''">
                <hr class="main_hr">
                <input class="__ON_INPUT__" placeholder="''' + await get_lang('regex') + '''" name="content" value="''' + html.escape(textarea) + '''" type="text">
            '''
        elif tool == 'name_filter':
            title = await get_lang('id_filter_add')
            form_data = '' + \
                await get_lang('regex') + \
                '<hr class="main_hr">' + \
                '<input class="__ON_INPUT__" value="' + html.escape(name) + '" type="text" name="title">' + \
            ''
        elif tool == 'file_filter':
            title = await get_lang('file_filter_add')
            form_data = '' + \
                await get_lang('regex') + \
                '<hr class="main_hr">' + \
                '<input class="__ON_INPUT__" value="' + html.escape(name) + '" type="text" name="title">' + \
            ''
        elif tool == 'email_filter':
            title = await get_lang('email_filter_add')
            form_data = '' + \
                await get_lang('email') + \
                '<hr class="main_hr">' + \
                '<input class="__ON_INPUT__" value="' + html.escape(name) + '" type="text" name="title">' + \
            ''
        elif tool == 'image_license':
            title = await get_lang('image_license_add')
            form_data = '' + \
                await get_lang('license') + \
                '<hr class="main_hr">' + \
                '<input class="__ON_INPUT__" value="' + html.escape(name) + '" type="text" name="title">' + \
            ''
        elif tool == 'extension_filter':
            title = await get_lang('extension_filter_add')
            form_data = '' + \
                await get_lang('extension') + \
                '<hr class="main_hr">' + \
                '<input class="__ON_INPUT__" value="' + html.escape(name) + '" type="text" name="title">' + \
                '<hr class="main_hr">' + \
                await get_lang('max_file_size') + ' (MB) (' + await get_lang('default') + ' : ' + await get_lang('empty') + ')' + \
                '<hr class="main_hr">' + \
                '<input class="__ON_INPUT__" value="" type="text" name="max_file_size">' + \
            ''
        elif tool == 'document':
            acl_list = await get_acl_list()
            
            db_data = html_filters.get(name, 'document')
            acl_list = [['selected' if db_data and db_data.plus_t == for_a else '', for_a] for for_a in acl_list]

            title = await get_lang('document_filter_add')
            form_data = '''
                ''' + await get_lang('name') + '''
                <hr class="main_hr">
                <input class="__ON_INPUT__" value="''' + html.escape(name) + '''" type="text" name="name">
                <hr class="main_hr">
                ''' + await get_lang('regex') + '''
                <hr class="main_hr">
                <input class="__ON_INPUT__" value="''' + (html.escape(db_data.plus) if db_data else '') + '''" type="text" name="regex">
                <hr class="main_hr">
                <a href="/acl/Test#exp">''' + await get_lang('acl') + '''</a>
                <hr class="main_hr">
                <span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="acl">
                    ''' + ''.join(['<option ' + for_a[0] + ' value=' + for_a[1] + '>' + ('normal' if for_a[1] == '' else for_a[1]) + '</option>' for for_a in acl_list]) + '''
                </select></span>
            '''
        elif tool == 'template':
            title = await get_lang('template_document_add')

            value = ''
            if name:
                exist = html_filters.get(name, 'template')
                value = exist.plus if exist else ''

            form_data = '' + \
                await get_lang('template') + \
                '<hr class="main_hr">' + \
                '<input class="__ON_INPUT__" value="' + html.escape(name) + '" type="text" name="title">' + \
                '<hr class="main_hr">' + \
                await get_lang('explanation') + \
                '<hr class="main_hr">' + \
                '<input class="__ON_INPUT__" value="' + html.escape(value) + '" type="text" name="exp">' + \
                '<hr class="main_hr">' + \
            ''
        else:
            title = await get_lang('edit_tool_add')
            
            value = ''
            if name:
                exist = html_filters.get(name, 'edit_top')
                value = exist.plus if exist else ''

            form_data = '''
                ''' + await get_lang('title') + '''
                <hr class="main_hr">
                <input class="__ON_INPUT__" value="''' + html.escape(name) + '''" type="text" name="title">
                <hr class="main_hr">
                ''' + await get_lang('markup') + '''
                <hr class="main_hr">
                <input class="__ON_INPUT__" value="''' + html.escape(value) + '''" type="text" name="markup">
            '''

        return await render_template(
            title,
            '''
                    <form method="post">
                        ''' + form_data + '''
                        <hr class="main_hr">
                        <button class="__ON_BUTTON__" ''' + stat + ''' type="submit">''' + await get_lang('add') + '''</button>
                    </form>
                    ''',
            get_sub,
            [['filter/' + tool, await get_lang('return')]]
        )
