from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.config.startup_options import get_init_set_list
from opennamu_forge.presentation.shared.func import (
    SettingKey,
    flask,
    get_acl_list,
    get_time,
    history_plus,
    html,
    ip_check,
    ip_or_user,
    re,
    re_error,
    render_set,
)
from opennamu_forge.presentation.text_helpers import cache_v
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    redirect,
    render_simple_set,
    render_template,
)
from opennamu_forge.presentation.dependencies import (
    get_document_meta_repository,
    get_wiki_document_repository,
    get_wiki_settings_service,
)
def view_set_markup(document_name = '', markup = '', addon = '', disable = ''):
    document_meta = get_document_meta_repository()
    wiki_settings = get_wiki_settings_service()

    default_markup = wiki_settings.get(SettingKey.MARKUP, default='namumark')

    markup_load = markup
    if markup == '':
        markup_load = document_meta.get(document_name, 'document_markup')

    markup_list = ['normal'] + get_init_set_list('markup')['list']
    markup_html = ''
    for for_a in markup_list:
        if markup_load == for_a:
            markup_html = '<option value="' + (for_a if for_a != 'normal' else default_markup) + '">' + for_a + '</option>' + markup_html
        else:
            markup_html += '<option value="' + (for_a if for_a != 'normal' else default_markup) + '">' + for_a + '</option>'
    
    markup_html = '<span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="document_markup" ' + disable + ' ' + addon + '>' + markup_html + '</select></span>'

    return markup_html

async def view_set(name = 'Test', multiple = False):
    document_meta = get_document_meta_repository()
    wiki_documents = get_wiki_document_repository()

    check_ok = ''
    ip = ip_check()
    time = get_time()

    if multiple and flask.request.method == 'POST':
        all_title = re.findall(r'([^\n]+)\n', flask.request.form.get('title_name', '').replace('\r', '') + '\n')
        for name in all_title:
            view_set(name, False)

        return redirect('/list/document/acl')
    else:
        if flask.request.method == 'POST':
            check_data = 'document_set (' + name + ')'
        else:
            check_data = ''

        need_admin = True

        user_data = re.search(r'^user:([^/]+)', name)
        if user_data:
            if ip_or_user(ip) != 0:
                return redirect('/login')

            if user_data.group(1) == ip:
                need_admin = False
        
        if need_admin:
            if await acl_check(tool = 'acl_auth') == 1:
                if flask.request.method == 'POST':
                    return await re_error(3)
                else:
                    check_ok = 'disabled'

    if flask.request.method == 'POST':
        acl_data = ['decu', 'document_edit_acl', 'document_edit_request_acl', 'document_move_acl', 'document_delete_acl', 'dis', 'view', 'why']
        acl_result = []
        acl_text = ''

        for i in acl_data:
            form_data = flask.request.form.get(i, '')
            
            acl_result += [form_data]

            acl_text += i + '\n'
            acl_text += form_data + '\n'
        
            document_meta.upsert_acl(name, i, form_data)
            
            document_meta.delete(name, 'acl_date', doc_rev=i)
                
            time_limit = flask.request.form.get(i + '_date', '')
            if re.search(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$', time_limit):
                document_meta.upsert(name, 'acl_date', time_limit, doc_rev=i)
                
                acl_text += time_limit + '\n'

            acl_text += '\n\n'

        markup_data = flask.request.form.get('document_markup', '')
        
        acl_text += 'document_markup\n'
        acl_text += markup_data + '\n\n'

        old_markup_data = document_meta.get(name, 'document_markup')

        document_meta.upsert(name, 'document_markup', markup_data)

        if old_markup_data != markup_data:
            doc_data = wiki_documents.get_data(name)
            if wiki_documents.exists_title(name):
                await render_set(
                    doc_name = name,
                    doc_data = doc_data,
                    data_type = 'backlink'
                )

        markup_data = markup_data if markup_data != '' else 'normal'

        if await acl_check('', 'owner_auth', '', '') != 1:
            document_top = flask.request.form.get('document_top', '')

            acl_text += 'document_top\n'
            acl_text += document_top + '\n\n'

            document_meta.upsert(name, 'document_top', document_top)
            
            document_editor_top = flask.request.form.get('document_editor_top', '')

            acl_text += 'document_editor_top\n'
            acl_text += document_editor_top + '\n\n'

            document_meta.upsert(name, 'document_editor_top', document_editor_top)

        if need_admin:
            await acl_check(tool = 'acl_auth', memo = check_data)

        history_plus(
            name,
            acl_text,
            time,
            ip,
            acl_result[7],
            '0',
            mode = 'setting'
        )

        return redirect('/acl/' + url_pas(name))
    else:
        data = '<h2>' + await get_lang('acl') + '</h2>'
        acl_list = await get_acl_list()
        acl_get_list = [
            [await get_lang('view_acl'), 'view', '3'],
            [await get_lang('document_acl'), 'decu', '4'],
            [await get_lang('document_edit_acl'), 'document_edit_acl', '5'],
            [await get_lang('document_edit_request_acl'), 'document_edit_request_acl', '5'],
            [await get_lang('document_move_acl'), 'document_move_acl', '5'],
            [await get_lang('document_delete_acl'), 'document_delete_acl', '5'],
            [await get_lang('discussion_acl'), 'dis', '3'],
        ]

        for i in acl_get_list:
            data += '' + \
                '<h' + i[2] + '>' + i[0] + '</h' + i[2] + '>' + \
                '<span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="' + i[1] + '" ' + check_ok + '>' + \
            ''

            acl_data = document_meta.get_acl(name, i[1])
            for data_list in acl_list:
                check = 'selected="selected"' if acl_data == data_list else ''
                data += '<option value="' + data_list + '" ' + check + '>' + (data_list if data_list != '' else 'normal') + '</option>'

            data += '</select></span>'
            data += '<hr class="main_hr">'
            
            date_value = ''
            
            date_value = document_meta.get(name, 'acl_date', doc_rev=i[1])
            
            data += '<input class="__ON_INPUT__" type="date" ' + check_ok + ' value="' + date_value + '" name="' + i[1] + '_date" pattern="\\d{4}-\\d{2}-\\d{2}">'
            data += '<hr class="main_hr">'

        acl_why = html.escape(document_meta.get_acl(name, 'why'))
        data += '' + \
            '<h3>' + await get_lang('why') + '</h3>' + \
            '<input class="__ON_INPUT__" value="' + acl_why + '" ' + check_ok + ' placeholder="' + await get_lang('why') + '" name="why" ' + check_ok + '>' + \
            '<hr class="main_hr">' + \
        ''

        data += '''
            <h3>''' + await get_lang('explanation') + '''</h3>
            <span id="exp"></span>
            <ul>
                <li>normal : ''' + await get_lang('unset') + '''</li>
                <li>admin : ''' + await get_lang('admin_acl') + '''</li>
                <li>user : ''' + await get_lang('member_acl') + '''</li>
                <li>50_edit : ''' + await get_lang('50_edit_acl') + '''</li>
                <li>all : ''' + await get_lang('all_acl') + '''</li>
                <li>email : ''' + await get_lang('email_acl') + '''</li>
                <li>owner : ''' + await get_lang('owner_acl') + '''</li>
                <li>ban : ''' + await get_lang('ban_acl') + '''</li>
                <li>before : ''' + await get_lang('before_acl') + '''</li>
                <li>30_day : ''' + await get_lang('30_day_acl') + '''</li>
                <li>ban_admin : ''' + await get_lang('ban_admin_acl') + '''</li>
                <li>not_all : ''' + await get_lang('not_all_acl') + '''</li>
                <li>90_day : ''' + await get_lang('90_day_acl') + '''</li>
                <li>up_to_level_3 : ''' + await get_lang('up_to_level_3') + '''</li>
                <li>up_to_level_10 : ''' + await get_lang('up_to_level_10') + '''</li>
            </ul>
            <h2>''' + await get_lang('markup') + '''</h2>
        '''

        data += view_set_markup(document_name = name, disable = check_ok)

        save_button = '<button class="__ON_BUTTON__" type="submit" ' + check_ok + '>' + await get_lang('save') + '</button>'
        if await acl_check('', 'owner_auth', '', '') == 1:
            check_ok = 'disabled'

        document_top = document_meta.get(name, 'document_top')

        document_editor_top = document_meta.get(name, 'document_editor_top')

        data += '''
            <h2>''' + await get_lang('document_top') + ''' (HTML)</h2>
            <textarea ''' + check_ok + ''' class="opennamu_forge_textarea_100 __ON_TEXTAREA__" name="document_top">''' + html.escape(document_top) + '''</textarea>
            
            <h2>''' + await get_lang('document_editor_top') + ''' (HTML)</h2>
            <textarea ''' + check_ok + ''' class="opennamu_forge_textarea_100 __ON_TEXTAREA__" name="document_editor_top">''' + html.escape(document_editor_top) + '''</textarea>
        '''
        data += '<hr class="main_hr">'

        text_area = ''
        if multiple == True:
            text_area = '<textarea class="opennamu_forge_textarea_500 __ON_TEXTAREA__" placeholder="' + await get_lang('many_delete_help') + '" name="title_name"></textarea><hr class="main_hr">'
            menu = [
                ['manager', await get_lang('admin')]
            ]
            title = await get_lang('mutiple_document_setting')
            sub = 0
        else:
            menu = [
                ['w/' + url_pas(name), await get_lang('return')], 
                ['acl_multiple', await get_lang('mutiple_document_setting')],
                ['manager', await get_lang('admin')]
            ]
            title = name
            sub = '(' + await get_lang('document_setting') + ')'
            save_button += ' <button class="__ON_BUTTON__" type="button" onclick="w_set_reset();" ' + check_ok + '>' + await get_lang('reset') + '</button>'

        return await render_template(
            title,
            '''
                <form method="post">
                    <script defer src="/views/main_css/js/route/w_set.js''' + cache_v() + '''"></script>
                    ''' + text_area + '''
                    ''' + await render_simple_set(data) + '''
                    ''' + save_button + '''
                </form>
            ''',
            sub,
            menu
        )
