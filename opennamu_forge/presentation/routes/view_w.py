from .tool.func import *

from .go_api_w_raw import api_w_raw
from .go_api_w_render import api_w_render

async def view_w(name = 'Test', do_type = '', doc_rev = ''):
    with get_db_connect() as conn:
        backlinks = get_backlink_repository()
        document_meta = get_document_meta_repository()
        history = get_history_repository()
        topics = get_topic_repository()
        user_settings = get_user_setting_repository()
        wiki_documents = get_wiki_document_repository()
        wiki_settings = get_wiki_settings_service()

        sub = 0
        history_color = 0
        menu = []

        user_doc = ''
        category_total = ''
        file_data = ''

        doc_type = ''
        redirect_to = None

        now_time = get_time()
        ip = ip_check()
            
        uppage = re.sub(r"/([^/]+)$", '', name)
        uppage = 0 if uppage == name else uppage

        topic = 1 if topics.exists_open_recent_discuss_title(name) else 0

        down = 1 if wiki_documents.exists_title_prefix(name + '/') else 0

        if re.search(r'^category:', name):
            name_view = name
            doc_type = 'category'

            category_doc = ''
            category_sub = ''

            count_sub_category = 0
            count_category = 0

            category_sql = backlinks.list_distinct_links_by_title_type(name, 'cat')
            for data in category_sql:
                link_view = data
                if get_main_skin_set(conn, flask.session, 'main_css_category_change_title', ip) != 'off':
                    db_data = backlinks.get_data(name, data, 'cat_view')
                    if db_data != '':
                        link_view = db_data
                        
                link_blur = ''
                if backlinks.exists(name, data, 'cat_blur'):
                    link_blur = 'opennamu_forge_category_blur'

                if data.startswith('category:'):
                    category_sub += '<li><a class="' + link_blur + '" href="/w/' + url_pas(data) + '">' + html.escape(link_view) + '</a></li>'
                    count_sub_category += 1
                else:
                    category_doc += '' + \
                        '<li>' + \
                            '<a class="' + link_blur + '" href="/w/' + url_pas(data) + '">' + html.escape(link_view) + '</a> ' + \
                            '<a class="opennamu_forge_link_inter" href="/xref/' + url_pas(data) + '">(' + await get_lang('backlink') + ')</a>' + \
                        '</li>' + \
                    ''
                    count_category += 1

            if category_sub != '':
                category_total += '' + \
                    '<h2 id="cate_under">' + await get_lang('under_category') + '</h2>' + \
                    '<ul>' + \
                        '<li>' + await get_lang('all') + ' : ' + str(count_sub_category) + '</li>' + \
                        category_sub + \
                    '</ul>' + \
                ''

            if category_doc != '':
                category_total += '' + \
                    '<h2 id="cate_normal">' + await get_lang('category_title') + '</h2>' + \
                    '<ul>' + \
                        '<li>' + await get_lang('all') + ' : ' + str(count_category) + '</li>' + \
                        category_doc + \
                    '</ul>' + \
                ''
        elif re.search(r"^user:([^/]*)", name):
            name_view = name
            doc_type = 'user'
            user_name = ''

            match = re.search(r"^user:([^/]*)", name)
            if match:
                user_name = html.escape(match.group(1))
            
            user_doc = ''

            # S admin or owner 특수 틀 추가
            if await acl_check(tool = 'all_admin_auth', ip = user_name) != 1:
                if await acl_check(tool = 'owner_auth', ip = user_name) != 1:
                    phrase_user_page_owner = wiki_settings.get(SettingKey.PHRASE_USER_PAGE_OWNER)
                    if phrase_user_page_owner != '':
                        user_doc += phrase_user_page_owner + '<br>'
                    else:
                        phrase_user_page_admin = wiki_settings.get(SettingKey.PHRASE_USER_PAGE_ADMIN)
                        if phrase_user_page_admin != '':
                            user_doc += phrase_user_page_admin + '<br>'
                else:
                    phrase_user_page_admin = wiki_settings.get(SettingKey.PHRASE_USER_PAGE_ADMIN)
                    if phrase_user_page_admin != '':
                        user_doc += phrase_user_page_admin + '<br>'
            # E
            
            user_doc += '''
                <div id="opennamu_forge_get_user_info">''' + html.escape(user_name) + '''</div>
                <hr class="main_hr">
            '''
            if name == 'user:' + user_name:
                menu += [['w/' + url_pas(name) + '/' + url_pas(now_time.split()[0]), await get_lang('today_doc')]]
        elif re.search(r"^file:", name):
            rev = history.latest_revision_id(name) or '1'

            name_view = name
            doc_type = 'file'

            mime_type = re.search(r'([^.]+)$', name)
            if mime_type:
                mime_type = mime_type.group(1)
            else:
                mime_type = 'jpg'

            file_name = re.sub(r'\.([^.]+)$', '', name)
            file_name = re.sub(r'^file:', '', file_name)

            file_all_name = sha224_replace(file_name) + '.' + mime_type
            file_path_name = os.path.join(load_image_url(conn), file_all_name)
            if os.path.exists(file_path_name):
                try:
                    img = Image.open(file_path_name)
                    width, height = img.size
                    file_res = str(width) + 'x' + str(height)
                except:
                    file_res = 'Vector'
                
                file_size = str(round(os.path.getsize(file_path_name) / 1000, 1))
                
                file_data = '''
                    <img src="/image/''' + url_pas(file_all_name) + '''.cache_v''' + rev + '''">
                    <h2>''' + await get_lang('data') + '''</h2>
                    <table>
                        <tr><td>''' + await get_lang('url') + '''</td><td><a href="/image/''' + url_pas(file_all_name) + '''">''' + await get_lang('link') + '''</a></td></tr>
                        <tr><td>''' + await get_lang('volume') + '''</td><td>''' + file_size + '''KB</td></tr>
                        <tr><td>''' + await get_lang('resolution') + '''</td><td>''' + file_res + '''</td></tr>
                    </table>
                    <h2>''' + await get_lang('content') + '''</h2>
                '''

                menu += [['delete_file/' + url_pas(name), await get_lang('file_delete')]]
            else:
                file_data = ''
        else:
            doc_type = 'include' if backlinks.has_include_title(name) else doc_type

            db_data = backlinks.get_redirect_for_link(name)
            if db_data:
                doc_type = 'redirect'

                if wiki_documents.exists_title(db_data[0]):
                    redirect_to = url_pas(db_data[0]) + db_data[1]

            name_view = name

        if doc_rev == '':
            doc_data = await api_w_raw(name)
        else:
            doc_data = await api_w_raw(name, str(doc_rev))

        # print([name, doc_data, doc_rev])

        length_doc_data = 0
        if doc_data["response"] == "ok":
            render_data = await api_w_render(name, request_method = 'POST', request_data = {
                'name' : name,
                'data' : doc_data["data"]
            })
            end_data = render_data["data"] + '<script>document.addEventListener("DOMContentLoaded", function() {' + render_data["js_data"] + '});</script>'
            length_doc_data = len(doc_data["data"])
        else:
            end_data = ''

        if doc_rev == '':
            await python_to_golang("get_json", path = "v2/page_view_post/" + url_pas(name))
            data = wiki_documents.get_data(name)
            data_exists = wiki_documents.exists_title(name)
        else:
            data = history.find_data(name, doc_rev)
            data_exists = data is not None

        description = ''
        if await acl_check(name, 'render') == 1:
            response_data = 401

            error_401 = wiki_settings.get(SettingKey.ERROR_401)
            if error_401 != '':
                end_data = '<h2>' + await get_lang('error') + '</h2><ul><li>' + error_401 + '</li></ul>'
            else:
                end_data = '<h2>' + await get_lang('error') + '</h2><ul><li>' + await get_lang('authority_error') + '</li></ul>'
        elif not data_exists:
            response_data = 404

            error_404 = wiki_settings.get(SettingKey.ERROR_404)
            if error_404 != '':
                end_data = '<h2>' + await get_lang('error') + '</h2><ul><li>' + error_404 + '</li></ul>'
            else:
                end_data = '<h2>' + await get_lang('error') + '</h2><ul><li>' + await get_lang('document_404_error') + '</li></ul>'

            history_color = 1 if history.exists_title(name) else 0
        else:
            response_data = 200
            description = data.replace('\r', '').replace('\n', ' ')[0:200]

        acl = 1 if document_meta.acl_title_exists(name) else 0
        menu_acl = 1 if await acl_check(name, 'document_edit') == 1 else 0
        if response_data == 404:
            menu += [['edit/' + url_pas(name), await get_lang('create'), menu_acl]] 
        else:
            menu += [['edit/' + url_pas(name), await get_lang('edit'), menu_acl]]

        menu += [
            ['topic/' + url_pas(name), await get_lang('discussion'), topic], 
            ['history/' + url_pas(name), await get_lang('history'), history_color], 
            ['xref/' + url_pas(name), await get_lang('backlink')], 
            ['acl/' + url_pas(name), await get_lang('setting'), acl],
        ]

        if flask.session and 'lastest_document' in flask.session:
            if type(flask.session['lastest_document']) != type([]):
                flask.session['lastest_document'] = []
        else:
            flask.session['lastest_document'] = []

        if do_type == 'from':
            menu += [['w/' + url_pas(name), await get_lang('pass')]]
            
            last_page = ''
            for for_a in reversed(range(0, len(flask.session['lastest_document']))):
                last_page = flask.session['lastest_document'][for_a]

                if backlinks.redirect_exists_for_title_or_link(last_page):
                    break

            if last_page != name:
                redirect_text = '{0} ➤ {1}'

                redirect_text_raw = wiki_settings.get(SettingKey.REDIRECT_TEXT)
                if redirect_text_raw != '':
                    redirect_text = redirect_text_raw

                try:
                    redirect_text = redirect_text.format('<a href="/w_from/' + url_pas(last_page) + '">' + html.escape(last_page) + '</a>', '<b>' + html.escape(name) + '</b>')
                except:
                    redirect_text = '{0} ➤ {1}'
                    redirect_text = redirect_text.format('<a href="/w_from/' + url_pas(last_page) + '">' + html.escape(last_page) + '</a>', '<b>' + html.escape(name) + '</b>')

                end_data = '''
                    <div class="opennamu_forge_redirect" id="redirect">
                        ''' + redirect_text + '''
                    </div>
                    <hr class="main_hr">
                ''' + end_data
                
        if len(flask.session['lastest_document']) >= 10:
            flask.session['lastest_document'] = flask.session['lastest_document'][-9:] + [name]
        else:
            flask.session['lastest_document'] += [name]
        
        flask.session['lastest_document'] = list(reversed(dict.fromkeys(reversed(flask.session['lastest_document']))))

        if redirect_to and do_type != 'from':
            return redirect(conn, '/w_from/' + redirect_to)

        view_history_on = get_main_skin_set(conn, flask.session, 'main_css_view_history', ip)
        if view_history_on == 'on':
            end_data = '' + \
                '<div class="opennamu_forge_trace">' + \
                    '<a class="opennamu_forge_trace_button" href="javascript:opennamu_forge_do_trace_spread();"> (+)</a>' + \
                    await get_lang('trace') + ' : ' + \
                    ' ← '.join(
                        [
                            '<a href="/w/' + url_pas(for_a) + '">' + html.escape(for_a) + '</a>'
                            for for_a in reversed(flask.session['lastest_document'])
                        ]
                    ) + \
                '</div>' + \
                '<hr class="main_hr">' + \
            '' + end_data

        if uppage != 0:
            menu += [['w/' + url_pas(uppage), await get_lang('upper')]]

        if down:
            menu += [['down/' + url_pas(name), await get_lang('sub')]]

        r_date = document_meta.get(name, 'last_edit') or 0

        div = file_data + user_doc + end_data + category_total
        
        if doc_type == '':
            outdated_doc_warning_date = wiki_settings.get(SettingKey.OUTDATED_DOC_WARNING_DATE)
            if outdated_doc_warning_date != '' and r_date != 0:
                time_1 = datetime.datetime.strptime(r_date, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(days = int(number_check(outdated_doc_warning_date)))
                time_2 = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
                if time_2 > time_1:
                    outdated_doc_warning = wiki_settings.get(SettingKey.OUTDATED_DOC_WARNING)
                    div = (outdated_doc_warning if outdated_doc_warning != '' else await get_lang('old_page_warning')) + '<hr class="main_hr">' + div

        body = wiki_settings.get(SettingKey.BODY)
        div = (body + div) if body != '' else div

        bottom_body = wiki_settings.get(SettingKey.BOTTOM_BODY)
        div += bottom_body if bottom_body != '' else ''

        body = document_meta.get(name, 'document_top')
        div = (body + div) if body != '' else div

        if ip_or_user(ip) == 0:
            watch_list = 2 if user_settings.user_data_exists(ip, name) else 1
            menu += [['star_doc_from/' + url_pas(name), ('☆' if watch_list == 1 else '★'), watch_list - 1]]
        else:
            watch_list = 0

        menu += [['doc_watch_list/1/' + url_pas(name), await get_lang('watchlist')]]

        if doc_rev != '':
            sub = '(' + str(doc_rev) + ')'

        view_count_data = await python_to_golang("get_json", path = "v2/page_view/" + url_pas(name))
        view_count = view_count_data['data']

        other_set = {}
        other_set['doc_name'] = name

        div += '<div class="opennamu_forge_clearfix"></div>'

        comment_api = await python_to_golang("api_w_comment", other_set = other_set)
        comment = comment_api['data']

        div += comment

        return await render_template(
            name_view,
            div,
            sub,
            menu,
            [r_date, watch_list, description, view_count],
            {
                "length_doc" : str(length_doc_data),
            }
        ), response_data
