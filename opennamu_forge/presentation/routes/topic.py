from opennamu_forge.presentation.captcha_helpers import captcha_post
from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.shared.func import (
    add_alarm,
    do_add_thread,
    do_edit_filter,
    do_edit_slow_check,
    do_reload_recent_thread,
    do_title_length_check,
    flask,
    get_time,
    html,
    ip_check,
    ip_or_user,
    re,
    re_error,
)
from opennamu_forge.presentation.text_helpers import cache_v
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    redirect,
    render_template,
)
from opennamu_forge.presentation.dependencies import (
    get_history_repository,
    get_topic_repository,
    get_user_setting_repository,
)
from .go_api_topic import api_topic_thread_pre_render

from .edit import edit_editor

async def topic(topic_num = 0, do_type = '', doc_name = 'Test'):
    history = get_history_repository()
    topics = get_topic_repository()
    user_settings = get_user_setting_repository()
    topic_num = str(topic_num)

    if topic_num == '0':
        name = await get_lang('make_new_topic')
        sub = await get_lang('make_new_topic')

        name_value = doc_name
        sub_value = ''
    else:
        recent_discuss = topics.get_recent_discuss(topic_num)
        if recent_discuss:
            sub = recent_discuss.subtitle
            name = recent_discuss.title

            name_value = name
            sub_value = sub
        else:
            return redirect('/')
            
    topic_acl = await acl_check(name_value, 'topic', topic_num)
    topic_view_acl = await acl_check('', 'topic_view', topic_num)
    if topic_view_acl == 1:
        return await re_error(0)
    elif topic_num == '0':
        if await acl_check('', 'discuss_make_new_thread', topic_num) == 1:
            return await re_error(0)

    ip = ip_check()

    if flask.request.method == 'POST' and do_type == '':
        if await do_edit_slow_check('thread') == 1:
            return await re_error(42)

        name = flask.request.form.get('topic', 'Test')
        sub = flask.request.form.get('title', 'Test')
        data = flask.request.form.get('content', 'Test').replace('\r', '')
        
        if do_title_length_check(name) == 1:
            return await re_error(38)
        
        if do_title_length_check(sub, 'topic') == 1:
            return await re_error(38)
        
        if await do_edit_filter(sub) == 1:
            return await re_error(21)
        
        if await do_edit_filter(data) == 1:
            return await re_error(21)
        
        if topic_num == '0':
            latest_topic_code = topics.latest_topic_code()
            topic_num = str(latest_topic_code + 1) if latest_topic_code else '1'
        
        if flask.request.form.get('content', 'Test') == '':
            return redirect('/thread/' + topic_num)

        if await captcha_post(flask.request.form.get('g-recaptcha-response', flask.request.form.get('g-recaptcha', ''))) == 1:
            return await re_error(13)

        today = get_time()

        if topic_acl == 1:
            return await re_error(0)

        old_num = topics.latest_comment_id(topic_num)
        num = str((old_num + 1) if old_num else 1)

        match = re.search(r'^user:([^/]+)', name)
        if match:
            match = match.group(1)
            y_check = 0
            if ip_or_user(match) == 1:
                if history.count_by_ip(match) > 0:
                    y_check = 1
                else:
                    if topics.count_by_ip(match) > 0:
                        y_check = 1
            else:
                if user_settings.id_exists(match):
                    y_check = 1

            if y_check == 1:
                await add_alarm(match, ip, '<a href="/thread/' + topic_num + '#' + num + '">' + html.escape(name) + ' - ' + html.escape(sub) + '#' + num + '</a>')
        
        ip_data = topics.first_comment_author(topic_num)
        if ip_data and ip_or_user(ip_data) == 0:
            await add_alarm(ip_data, ip, '<a href="/thread/' + topic_num + '#' + num + '">' + html.escape(name) + ' - ' + html.escape(sub) + '#' + num + '</a>')

        data = await api_topic_thread_pre_render(data, num, ip, topic_num, name, sub)

        do_add_thread(
            topic_num,
            data,
            '',
            num
        )
        do_reload_recent_thread(
            topic_num, 
            today, 
            name, 
            sub
        )

        return redirect('/thread/' + topic_num + '#' + num)
    else:
        acl_display = 'display: none;' if topic_acl == 1 else ''
        name_display = 'display: none;' if topic_num != '0' else ''

        shortcut = '<div class="opennamu_forge_thread_shortcut" id="thread_shortcut">'
        db_data = topics.list_comment_ids_ascending(topic_num)
        for for_a in db_data:
            shortcut += '<a href="#' + for_a + '">#' + for_a + '</a> '
        
        shortcut += '</div>'

        return await render_template(
            name,
            '''
                <script defer src="/views/main_css/js/route/topic.js''' + cache_v() + '''"></script>
                <style id="opennamu_forge_list_hidden_style">.opennamu_forge_list_hidden { display: none; }</style>
                <label class="__ON_CHECKLABEL__"><input class="__ON_CHECKBOX__" type="checkbox" onclick="opennamu_forge_list_hidden_remove();" checked> ''' + await get_lang('remove_hidden') + '''</label>
                <hr class="main_hr">

                ''' + shortcut + '''
                <h2 id="topic_top_title">''' + html.escape(sub) + '''</h2>
                
                <div id="opennamu_forge_top_thread"></div>
                <div id="opennamu_forge_main_thread"></div>
                <div id="opennamu_forge_reload_thread"></div>
                <script>
                    window.addEventListener("DOMContentLoaded", function() { 
                        opennamu_forge_get_thread("''' + topic_num + '''", "top");
                        opennamu_forge_get_thread("''' + topic_num + '''");
                    });
                </script>

                <a href="javascript:opennamu_forge_thread_blind();">(''' + await get_lang('hide') + ''' | ''' + await get_lang('hide_release') + ''')</a> 
                <a href="javascript:opennamu_forge_thread_delete();">(''' + await get_lang('delete') + ''')</a>
                <a href="/thread/''' + topic_num + '/tool">(' + await get_lang('topic_tool') + ''')</a>
                <hr class="main_hr">
                
                <form style="''' + acl_display + '''" method="post">
                    <div style="''' + name_display + '''">
                        <input class="__ON_INPUT__" placeholder="''' + await get_lang('document_name') + '''" name="topic" value="''' + html.escape(name_value) + '''">
                        <hr class="main_hr">
                        <input class="__ON_INPUT__" placeholder="''' + await get_lang('discussion_name') + '''" name="title" value="''' + html.escape(sub_value) + '''">
                        <hr class="main_hr">
                    </div>
                    
                    ''' + await edit_editor(ip, '', 'thread') + '''
                </form>
            ''',
            '(' + await get_lang('discussion') + ')',
            [['topic/' + url_pas(name), await get_lang('list')]]
        )
