# Init
import os
import sys
import datetime
import ipaddress
import html
import random
import subprocess
import threading
import time

if sys.version_info < (3, 10):
    raise RuntimeError('OpenNamu Forge requires Python 3.10 or newer.')

from opennamu_forge.infrastructure.logging import get_logger
from opennamu_forge.application.version import VERSION_INFO
from opennamu_forge.application.dto.settings import SettingKey
from opennamu_forge.presentation.dependencies import (
    get_document_meta_repository,
    get_history_repository,
    get_html_filter_repository,
    get_other_setting_repository,
    get_recent_block_repository,
    get_topic_repository,
    get_user_agent_repository,
    get_user_setting_repository,
    get_wiki_document_repository,
)
from opennamu_forge.presentation.authorization_helpers import (
    acl_check as _acl_check,
    ban_check as _ban_check,
)
from opennamu_forge.presentation.gopennamu_gateway import python_to_golang
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    http_warning,
    load_domain,
    load_lang,
    redirect,
    render_simple_set,
    render_template,
)
from opennamu_forge.presentation.text_helpers import (
    cache_v,
    cut_100,
    get_tool_js_safe,
    leng_check,
    number_check,
)

logger = get_logger(__name__)

# Init-Version
version_list = VERSION_INFO

logger.info('Version : %s', version_list['r_ver'])
logger.info('DB set version : %s', version_list['c_ver'])
logger.info('Skin set version : %s', version_list['s_ver'])

# Init-Version Marker
os.makedirs("data", exist_ok=True)
logger.info('uv-managed dependencies are expected. Run "uv sync --extra performance --extra dev" before startup.')

# Init-Load
from .sql_dialect import (
    get_main_skin_set,
    get_time,
    hashlib,
    ip_check,
    ip_or_user,
    re,
)
from opennamu_forge.presentation.rendering.renderer import class_do_render

from diff_match_patch import diff_match_patch

import werkzeug.routing
import werkzeug.debug

import flask
import asyncio
import nest_asyncio

import requests
import psutil
from PIL import Image

if sys.version_info < (3, 6):
    import sha3

class flask_data_or_variable:
    def __init__(self, flask_data, var_dict):
        if var_dict == {}:
            self.data = flask_data
            self.selected_flask = True
        else:
            self.data = var_dict
            self.selected_flask = False

    def get(self, dict_name, replace_data):
        if self.selected_flask == True:
            return self.data.get(dict_name, replace_data)
        else:
            if dict_name in self.data:
                return self.data[dict_name]
            else:
                return replace_data

async def opennamu_forge_make_list(left = '', right = '', bottom = '', class_name = ''):
    data_html = f'<span class="{class_name}">'
    data_html += '<div class="opennamu_forge_recent_change">'
    data_html += left

    data_html += '<div style="float: right;">'
    data_html += right
    data_html += '</div>'

    data_html += '<div style="clear: both;"></div>'

    if bottom != '':
        data_html += '<hr>'
        data_html += bottom

    data_html += '</div>'
    data_html += '<hr class="main_hr">'
    data_html += '</span>'

    return data_html

# Func-init
def get_db_table_list():
    # DB table
    # Init-Create_DB
    
    # --이거 개편한다더니 도대체 언제?--
    create_data = {}

    # 폐지 예정 (data_set으로 통합)
    create_data['data_set'] = ['doc_name', 'doc_rev', 'set_name', 'set_data']
    
    create_data['data'] = ['title', 'data', 'type']
    create_data['history'] = ['id', 'title', 'data', 'date', 'ip', 'send', 'leng', 'hide', 'type']
    create_data['rc'] = ['id', 'title', 'date', 'type']
    create_data['acl'] = ['title', 'data', 'type']

    # 개편 예정 (data_link로 변경)
    create_data['back'] = ['title', 'link', 'type', 'data']

    # 폐지 예정 (topic_set으로 통합) [가장 시급]
    create_data['topic_set'] = ['thread_code', 'set_name', 'set_id', 'set_data']

    create_data['rd'] = ['title', 'sub', 'code', 'date', 'band', 'stop', 'agree', 'acl']
    create_data['topic'] = ['id', 'data', 'date', 'ip', 'block', 'top', 'code']

    # 폐지 예정 (user_set으로 통합)
    create_data['rb'] = ['block', 'end', 'today', 'blocker', 'why', 'band', 'login', 'ongoing']

    # 개편 예정 (wiki_set과 wiki_filter과 wiki_vote으로 변경)
    create_data['other'] = ['name', 'data', 'coverage']
    create_data['html_filter'] = ['html', 'kind', 'plus', 'plus_t']
    create_data['vote'] = ['name', 'id', 'subject', 'data', 'user', 'type', 'acl']

    # 개편 예정 (auth와 auth_log로 변경)
    create_data['alist'] = ['name', 'acl']
    create_data['re_admin'] = ['who', 'what', 'time']

    # 개편 예정 (user_notice와 user_agent로 변경)
    create_data['ua_d'] = ['name', 'ip', 'ua', 'today', 'sub']

    create_data['user_set'] = ['name', 'id', 'data']
    create_data['user_notice'] = ['id', 'name', 'data', 'date', 'readme']

    create_data['bbs_set'] = ['set_name', 'set_code', 'set_id', 'set_data']
    create_data['bbs_data'] = ['set_name', 'set_code', 'set_id', 'set_data']
    
    return create_data

# Func-simple
## Func-simple-without_DB
def get_default_admin_group():
    return ['owner', 'user', 'ip', 'ban']

async def get_next_page_bottom(link, num, page, end = 50):
    list_data = ''

    if num == 1:
        if len(page) == end:
            list_data += '' + \
                '<hr class="main_hr">' + \
                '<a href="' + link.format(str(num + 1)) + '">(' + await get_lang('next') + ')</a>' + \
            ''
    elif len(page) != end:
        list_data += '' + \
            '<hr class="main_hr">' + \
            '<a href="' + link.format(str(num - 1)) + '">(' + await get_lang('previous') + ')</a>' + \
        ''
    else:
        list_data += '' + \
            '<hr class="main_hr">' + \
            '<a href="' + link.format(str(num - 1)) + '">(' + await get_lang('previous') + ')</a> ' + \
            '<a href="' + link.format(str(num + 1)) + '">(' + await get_lang('next') + ')</a>' + \
        ''

    return list_data

# Golang 의존
async def get_acl_list(type_data = 'normal'):
    if type_data == 'user':
        type_data = 'user_document'

    other_set = {}
    other_set['type'] = type_data

    data = await python_to_golang('api_list_acl', other_set)

    return data["data"]

## Func-simple-with_DB
async def get_user_title_list(ip = ''):
    ip = ip_check() if ip == '' else ip

    # default
    user_title = {
        '' : await get_lang('default'),
        '🌳' : '🌳 newbie',
    }

    user_settings = get_user_setting_repository()

    if user_settings.exists(ip, 'get_🥚'):
        user_title['🥚'] = '🥚 easter_egg'

    if user_settings.exists(ip, 'challenge_first_contribute'):
        user_title['🔰'] = '🔰 first_contribute'

    if user_settings.exists(ip, 'challenge_tenth_contribute'):
        user_title['📝'] = '📝 tenth_contribute'

    if user_settings.exists(ip, 'challenge_hundredth_contribute'):
        user_title['🖊️'] = '🖊️ hundredth_contribute'

    if user_settings.exists(ip, 'challenge_thousandth_contribute'):
        user_title['🏅'] = '🏅 thousandth_contribute'

    if user_settings.exists(ip, 'challenge_first_discussion'):
        user_title['💬'] = '💬 first_discussion'

    if user_settings.exists(ip, 'challenge_tenth_discussion'):
        user_title['💡'] = '💡 tenth_discussion'

    if user_settings.exists(ip, 'challenge_hundredth_discussion'):
        user_title['📢'] = '📢 hundredth_discussion'

    if user_settings.exists(ip, 'challenge_thousandth_discussion'):
        user_title['📜'] = '📜 thousandth_discussion'

    if user_settings.exists(ip, 'challenge_admin'):
        user_title['☑️'] = '☑️ before_admin'

    if await _acl_check(tool = 'all_admin_auth') != 1:
        user_title['✅'] = '✅ admin'
    
    return user_title
    
async def edit_button():
    insert_list = []

    db_data = get_html_filter_repository().list_by_kind('edit_top')
    for get_data in db_data:
        insert_list += [[get_data.plus, get_data.html]]

    data = ''
    for insert_data in insert_list:
        data += '<a href="javascript:do_insert_data(\'' + get_tool_js_safe(insert_data[0]) + '\');">(' + html.escape(insert_data[1]) + ')</a> '

    data += (' ' if data != '' else '') + '<a href="/filter/edit_top">(' + await get_lang('add') + ')</a>'
    data += '<hr class="main_hr">'
    
    return data

async def ip_warning():
    if ip_or_user() != 0:
        data = get_other_setting_repository().get('no_login_warning')
        if data != '':
            text_data = '' + \
                '<span>' + data + '</span>' + \
                '<hr class="main_hr">' + \
            ''
        else:
            text_data = '' + \
                '<span>' + await get_lang('no_login_warning') + '</span>' + \
                '<hr class="main_hr">' + \
            ''
    else:
        text_data = ''

    return text_data
    
# Func-login    
def pw_encode(data, db_data_encode = ''):
    if db_data_encode == '':
        db_data_encode = get_other_setting_repository().get('encode', default='sha3')

    if db_data_encode == 'sha256':
        return hashlib.sha256(bytes(data, 'utf-8')).hexdigest()
    elif db_data_encode == 'sha3':
        return hashlib.sha3_256(bytes(data, 'utf-8')).hexdigest()
    elif db_data_encode == 'sha3-512':
        return hashlib.sha3_512(bytes(data, 'utf-8')).hexdigest()
    else:
        db_data_salt = get_other_setting_repository().get('salt_key')
        
        if db_data_encode == 'sha3-salt':
            return hashlib.sha3_256(bytes(data + db_data_salt, 'utf-8')).hexdigest()
        else:
            return hashlib.sha3_512(bytes(data + db_data_salt, 'utf-8')).hexdigest()

def pw_check(data, data2, type_d = 'no', id_d = ''):
    load_set_data = get_other_setting_repository().get('encode') or 'sha3'
    
    set_data = load_set_data
    if type_d != 'no':
        set_data = 'sha3' if type_d == '' else type_d

    re_data = 1 if pw_encode(data, set_data) == data2 else 0
    if load_set_data != set_data and re_data == 1 and id_d != '':
        user_settings = get_user_setting_repository()
        user_settings.upsert(id_d, 'pw', pw_encode(data))
        user_settings.upsert(id_d, 'encode', load_set_data)

    return re_data
        
async def skin_check(set_n = 0):
    other_set = {}
    other_set["set_n"] = str(set_n)

    res = await python_to_golang('api_func_skin_name', other_set)
    raw = res["data"]

    norm = os.path.normpath(raw)
    parts = norm.split(os.sep)
    if "views" in parts:
        idx = parts.index("views")
        rel_parts = parts[idx + 1:]
    else:
        rel_parts = parts

    data = "/".join(rel_parts)

    return data
    
async def wiki_set():
    other_set = {}

    data = await python_to_golang('api_func_wiki_set', other_set)

    return data["data"]

async def wiki_custom():
    other_set = {}

    data = await python_to_golang('api_func_wiki_custom', other_set)

    return data["data"]

async def load_skin(data = '', set_n = 0, default = 0):
    # without_DB

    # data -> 가장 앞에 있을 스킨 이름
    # set_n == 0 -> 스트링으로 반환
    # set_n == 1 -> 리스트로 반환
    # default == 0 -> 디폴트 미포함
    # default == 1 -> 디폴트 포함

    skin_return_data = []
    skin_return_data_str = ''

    skin_list_get = os.listdir('views')
    if default == 1:
        skin_list_get = ['default'] + skin_list_get

    for skin_data in skin_list_get:
        if skin_data != 'default':
            see_data = skin_data
        else:
            see_data = await get_lang('default')

        if skin_data != 'main_css':
            if set_n == 0:
                if skin_data == data:
                    skin_return_data_str = '' + \
                        '<option value="' + skin_data + '">' + \
                            see_data + \
                        '</option>' + \
                    '' + skin_return_data_str
                else:
                    skin_return_data_str += '' + \
                        '<option value="' + skin_data + '">' + \
                            see_data + \
                        '</option>' + \
                    ''
            else:
                if skin_data == data:
                    skin_return_data = [skin_data] + skin_return_data
                else:
                    skin_return_data += [skin_data]                    

    if set_n == 0:
        return skin_return_data_str
    else:
        return skin_return_data

# Func-markup
async def render_set(doc_name = '', doc_data = '', data_type = 'view', markup = '', parameter = {}):
    # data_type in ['view', 'from', 'thread', 'api_view', 'api_thread', 'api_include', 'backlink']
    # data_type을 list 형식으로 개편 필요할 듯

    return_type = True
    if data_type in ['api_from', 'api_view', 'api_thread', 'api_include']:
        return_type = False

    if await _acl_check(doc_name, 'render') == 1:
        if not return_type:
            return ["", ""]
        else:
            return ''

    if data_type == '':
        data_type = 'view'
    elif data_type == 'api_view':
        data_type = 'view'
    elif data_type == 'api_from':
        data_type = 'from'
    elif data_type == 'api_thread':
        data_type = 'thread'
    elif data_type == 'api_include':
        data_type = 'include'

    doc_data = '' if doc_data == None else doc_data

    ip = ip_check()
    render_lang_data = {
        'toc' : await get_lang('toc'),
        'category' : await get_lang('category')
    }

    db_data = get_other_setting_repository().get('category_text')
    if db_data != '':
        render_lang_data['category'] = db_data

    get_class_render = await class_do_render(
        render_lang_data,
        markup,
        parameter,
        render_set
    ).do_render(
        doc_name,
        doc_data,
        data_type
    )
    if data_type == 'backlink':
        return ''

    get_class_render[0] = '<div class="opennamu_forge_render_complete">' + get_class_render[0] + '</div>'

    font_size_set_data = get_main_skin_set(flask.session, 'main_css_font_size', ip)
    if font_size_set_data != 'default':
        font_size_set_data = number_check(font_size_set_data)

        get_class_render[0] = '' + \
            '''<style>
                .opennamu_forge_render_complete {
                    font-size: ''' + font_size_set_data + '''px !important;
                }
            </style>''' + \
        '' + get_class_render[0]

    db_data = get_other_setting_repository().get('namumark_compatible')
    if db_data != '':
        get_class_render[0] = '' + \
            '''<style>
                .opennamu_forge_render_complete {
                    font-size: 15px !important;
                    line-height: 1.5;
                }

                .opennamu_forge_render_complete td {
                    padding: 5px 10px !important;
                    word-break: break-all;
                }

                .opennamu_forge_render_complete summary {
                    list-style: none !important;
                    font-weight: bold !important;
                }

                .opennamu_forge_render_complete .opennamu_forge_folding {
                    margin-bottom: 5px;
                }

                .opennamu_forge_render_complete .opennamu_forge_footnote {
                    padding-bottom: 30px;
                }

                .opennamu_forge_render_complete iframe {
                    display: block;
                }
            </style>''' + \
        '' + get_class_render[0]

    table_set_data = get_main_skin_set(flask.session, 'main_css_table_scroll', ip)
    if table_set_data == 'on':
        get_class_render[0] = '<style>.table_safe { overflow-x: scroll; white-space: nowrap; }</style>' + get_class_render[0]

    joke_set_data = get_main_skin_set(flask.session, 'main_css_view_joke', ip)
    if joke_set_data == 'off':
        get_class_render[0] = '<style>.opennamu_forge_joke { display: none; }</style>' + get_class_render[0]

    math_set_data = get_main_skin_set(flask.session, 'main_css_math_scroll', ip)
    if math_set_data == 'on':
        get_class_render[0] = '<style>.katex .base { overflow-x: scroll; }</style>' + get_class_render[0]

    transparent_set_data = get_main_skin_set(flask.session, 'main_css_table_transparent', ip)
    if transparent_set_data == 'on':
        get_class_render[0] = '' + \
            '''<style>
                .table_safe td {
                    background: transparent !important;
                    color: inherit !important;
                }
            </style>''' + \
        '' + get_class_render[0]

    if not return_type:
        return [get_class_render[0], get_class_render[1]]
    else:
        return get_class_render[0] + '<script>window.addEventListener("DOMContentLoaded", function() {' + get_class_render[1] + '});</script>'
        
# Func-edit
def get_edit_text_bottom(tool = '') :
    settings = get_other_setting_repository()
    b_text = ''
    
    db_data = settings.get('edit_bottom_text')
    if db_data != '':
        b_text = db_data + '<hr class="main_hr">'

    if tool != '':
        if tool == 'edit':
            db_data = settings.get('edit_only_bottom_text')
        elif tool == 'move':
            db_data = settings.get('move_bottom_text')
        elif tool == 'delete':
            db_data = settings.get('delete_bottom_text')
        else:
            db_data = settings.get('revert_bottom_text')

        if db_data != '':
            b_text = db_data + '<hr class="main_hr">'

    return b_text

def get_edit_text_bottom_check_box():
    cccb_text = ''

    sql_d = get_other_setting_repository().get('copyright_checkbox_text')
    if sql_d != '':
        checked = ''
        if flask.session and 'bottom_check_box_pass' in flask.session:
            checked = 'checked'

        cccb_text = '' + \
            '<label class="__ON_CHECKLABEL__"><input class="__ON_CHECKBOX__" type="checkbox" name="copyright_agreement" value="yes" ' + checked + '> ' + sql_d + '</label>' + \
            '<hr class="main_hr">' + \
        ''
        
    return cccb_text

def do_edit_text_bottom_check_box_check(data):
    db_data = get_other_setting_repository().get('copyright_checkbox_text')
    if db_data != '':
        if 'bottom_check_box_pass' in flask.session and flask.session['bottom_check_box_pass'] > 0:
            pass
        elif data != 'yes':
            return 1

    if not 'bottom_check_box_pass' in flask.session:
        flask.session['bottom_check_box_pass'] = 1
        
    return 0

async def do_edit_send_check(data):
    db_data = get_other_setting_repository().get('edit_bottom_compulsion')
    if db_data != '':
        if await _acl_check('', 'edit_bottom_compulsion') == 1:
            if data == '':
                return 1
    
    return 0

async def do_edit_slow_check(do_type = 'edit'):
    settings = get_other_setting_repository()

    if do_type == 'edit':
        slow_edit = settings.get('slow_edit')
    else:
        # do_type == 'thread'
        slow_edit = settings.get('slow_thread')
    
    if slow_edit != '':
        if await _acl_check('', 'slow_edit') == 1:
            slow_edit = int(number_check(slow_edit))

            if do_type == 'edit':
                last_edit_data = get_history_repository().latest_date_by_ip(ip_check())
            else:
                last_edit_data = get_topic_repository().latest_date_by_ip(ip_check())
            
            if last_edit_data:
                last_edit_data = int(re.sub(' |:|-', '', last_edit_data))
                now_edit_data = int((
                    datetime.datetime.now() - datetime.timedelta(seconds = slow_edit)
                ).strftime("%Y%m%d%H%M%S"))

                if last_edit_data > now_edit_data:
                    return 1

    return 0

async def do_edit_filter(data):
    ip = ip_check()
    if await _acl_check(tool = 'edit_filter_pass') == 1:
        for data_list in get_html_filter_repository().list_regex_filters_with_plus():
            match = re.compile(data_list.plus, re.I)
            if match.search(data):
                end = '0' if data_list.plus_t == 'X' else data_list.plus_t

                if end != '0':
                    end = int(number_check(end))
                    time = datetime.datetime.now()
                    plus = datetime.timedelta(seconds = end)
                    r_time = (time + plus).strftime("%Y-%m-%d %H:%M:%S")
                else:
                    r_time = '0'

                get_user_setting_repository().upsert(ip, 'edit_filter', data)

                ban_insert(
                    ip,
                    r_time,
                    'edit filter',
                    '',
                    'tool:edit filter'
                )

                return 1

    return 0

def do_title_length_check(name, check_type = 'document'):
    settings = get_other_setting_repository()
    
    if check_type == 'topic':
        db_data = settings.get('title_topic_max_length')
        if db_data != '':
            db_data = int(number_check(db_data))
            if len(name) > db_data:        
                return 1
    else:
        db_data = settings.get('title_max_length')
        if db_data != '':
            db_data = int(number_check(db_data))
            if len(name) > db_data:        
                return 1
    
    return 0

# Func-insert
def do_add_thread(thread_code, thread_data, thread_top = '', thread_id = ''):
    topics = get_topic_repository()
    
    if thread_id == '':
        db_data = topics.latest_comment_id(thread_code)
        if db_data is not None:
            thread_id = str(db_data + 1)
        else:
            thread_id = '1'
        
    topics.add_comment(
        thread_code,
        thread_id,
        thread_data,
        get_time(),
        ip_check(),
        thread_top,
    )
    
def do_reload_recent_thread(topic_num, date, name = None, sub = None):
    topics = get_topic_repository()

    if topics.update_recent_discuss_date(topic_num, date):
        pass
    else:
        topics.add_recent_discuss(topic_num, name, sub, date)

async def add_alarm(to_user, from_user, context):
    other_set = {}
    other_set['to'] = to_user
    other_set['from'] = from_user
    other_set['data'] = context

    await python_to_golang('api_func_alarm_post', other_set)

def add_user(user_name, user_pw, user_email = '', user_encode = ''):
    user_settings = get_user_setting_repository()

    if user_encode == '':
        user_pw_hash = pw_encode(user_pw)
        data_encode = get_other_setting_repository().get('encode', default='sha3')
    else:
        user_pw_hash = user_pw
        data_encode = user_encode

    if not user_settings.has_any():
        user_auth = 'owner'
    else:
        user_auth = 'user'

    user_settings.add(user_name, 'pw', user_pw_hash)
    user_settings.add(user_name, 'acl', user_auth)
    user_settings.add(user_name, 'date', get_time())
    user_settings.add(user_name, 'encode', data_encode)
    
    if user_email != '':
        user_settings.add(user_name, 'email', user_email)
    
def ua_plus(u_id, u_ip, u_agent, time):
    rep_data = get_other_setting_repository().get('ua_get')
    if rep_data != '':
        pass
    else:
        get_user_agent_repository().add(u_id, u_ip, u_agent, time)

def ban_insert(name, end, why, login, blocker, type_d = None, release = 0):
    now_time = get_time()
    band = type_d if type_d else ''
    recent_blocks = get_recent_block_repository()

    recent_blocks.close_ongoing(name, band)
    if release == 1:
        recent_blocks.add_record(
            name,
            'release',
            now_time,
            blocker,
            why,
            band,
            '',
            '',
        )
    else:
        login = login if login != '' else ''
        r_time = end if end != '0' else ''

        recent_blocks.add_record(
            name, 
            r_time, 
            now_time, 
            blocker, 
            why, 
            band,
            '1',
            login,
        )

def history_plus_rc_max(mode):
    history = get_history_repository()

    if history.count_recent_changes_by_type(mode) >= 200:
        rc_data = history.oldest_recent_change_ref_by_type(mode)
        if rc_data:
            history.delete_recent_change(rc_data[1], rc_data[0], mode)

def history_plus(title, data, date, ip, send, leng, t_check = '', mode = ''):
    history = get_history_repository()
    document_meta = get_document_meta_repository()
    
    db_data = get_other_setting_repository().get('history_recording_off')
    if db_data != '':
        return 0

    if mode == 'add' or mode == 'setting':
        id_data = history.earliest_revision_id(title)
        id_data = str(int(id_data) - 1) if id_data else '0'
    else:
        id_data = history.latest_revision_id(title)
        id_data = str(int(id_data) + 1) if id_data else '1'
        
        mode = 'r1' if id_data == '1' else mode
        if re.search('^user:', title):
            mode = 'user'
        elif re.search('^file:', title):
            mode = 'file'
        elif re.search('^category:', title):
            mode = 'category'

    send = re.sub(r'<|>', '', send)
    send = send[:512] if len(send) > 512 else send
    send = send + ' (' + t_check + ')' if t_check != '' else send

    if mode != 'add' and mode != 'setting' and mode != 'user':
        history_plus_rc_max('normal')

        history.add_recent_change(title, id_data, date, 'normal')
    
    if mode != 'add' and mode != 'setting':
        history_plus_rc_max(mode)

        count_data = get_wiki_document_repository().count_all_titles()
        get_other_setting_repository().upsert('count_all_title', str(count_data))

        history.add_recent_change(title, id_data, date, mode)

        data_set_exist = ''
        if mode == 'delete':
            data_set_exist = 'not_exist'

        document_meta.delete(title, 'edit_request_doing')

        document_meta.upsert(title, 'last_edit', date)

        document_meta.upsert(title, 'length', str(len(data)))

        document_meta.update_revision_marker(title, data_set_exist)

    history.add_history(title, id_data, data, date, ip, send, leng, mode)

# Func-error
async def re_error(data):
    if data == 0:
        if (await _ban_check())[0] == 1:
            end = '<div id="opennamu_forge_get_user_info">' + html.escape(ip_check()) + '</div>'
        else:
            end = '<ul><li>' + await get_lang('authority_error') + '</li></ul>'

        return await render_template(
            await get_lang('error'),
            '<h2>' + await get_lang('error') + '</h2>' + end,
            0,
            0
        ), 401
    else:
        title = await get_lang('error')
        sub_title = title
        return_code = 400

        num = data
        if num == 1:
            data = await get_lang('no_login_error')
        elif num == 2:
            data = await get_lang('no_exist_user_error')
        elif num == 3:
            data = await get_lang('authority_error')
        elif num == 4:
            data = await get_lang('no_admin_block_error')
        elif num == 5:
            data = await get_lang('error_skin_set')
        elif num == 8:
            data = '' + \
                await get_lang('long_id_error') + '<br>' + \
                await get_lang('id_char_error') + ' <a href="/filter/name_filter">(' + await get_lang('id_filter_list') + ')</a><br>' + \
                await get_lang('same_id_exist_error') + \
            ''
        elif num == 9:
            data = await get_lang('file_exist_error')
        elif num == 10:
            data = await get_lang('password_error')
        elif num == 11:
            data = await get_lang('topic_long_error')
        elif num == 12:
            data = await get_lang('email_error')
        elif num == 13:
            data = await get_lang('recaptcha_error')
        elif num == 14:
            data = await get_lang('file_extension_error') + ' <a href="/filter/extension_filter">(' + await get_lang('extension_filter_list') + ')</a>'
        elif num == 15:
            data = await get_lang('edit_record_error')
        elif num == 16:
            data = await get_lang('same_file_error')
        elif num == 17:
            db_data = get_other_setting_repository().get('upload')
            file_max = number_check(db_data) if db_data != '' else '2'
            data = await get_lang('file_capacity_error') + file_max
        elif num == 18:
            data = await get_lang('email_send_error')
        elif num == 19:
            data = await get_lang('move_error')
        elif num == 20:
            data = await get_lang('password_diffrent_error')
        elif num == 21:
            data = await get_lang('edit_filter_error')
        elif num == 22:
            data = await get_lang('file_name_error')
        elif num == 23:
            data = await get_lang('regex_error')
        elif num == 24:
            db_data = get_other_setting_repository().get('slow_edit')
            data = await get_lang('fast_edit_error') + db_data
        elif num == 25:
            data = await get_lang('too_many_dec_error')
        elif num == 26:
            data = await get_lang('application_not_found')
        elif num == 27:
            data = await get_lang("invalid_password_error")
        elif num == 28:
            data = await get_lang('watchlist_overflow_error')
        elif num == 29:
            data = await get_lang('copyright_disagreed')
        elif num == 30:
            data = await get_lang('ie_wrong_callback')
        elif num == 33:
            data = await get_lang('restart_fail_error')
        elif num == 35:
            data = await get_lang('same_email_error')
        elif num == 36:
            data = await get_lang('input_email_error')
        elif num == 37:
            data = await get_lang('error_edit_send_request')
        elif num == 38:
            db_data = get_other_setting_repository().get('title_max_length')
            data = await get_lang('error_title_length_too_long') + db_data
        elif num == 39:
            db_data = get_other_setting_repository().get('title_topic_max_length')
            data = await get_lang('error_title_length_too_long') + db_data
        elif num == 40:
            password_min_length = get_other_setting_repository().get('password_min_length')
            data = await get_lang('error_password_length_too_short') + password_min_length
        elif num == 41:
            db_data = get_other_setting_repository().get('edit_timeout')
            data = await get_lang('timeout_error') + db_data
        elif num == 42:
            db_data = get_other_setting_repository().get('slow_thread')
            data = await get_lang('fast_edit_error') + db_data
        elif num == 43:
            title = await get_lang('application_submitted')
            sub_title = title
            data = await get_lang('waiting_for_approval')
        elif num == 44:
            db_data = get_other_setting_repository().get('document_content_max_length')
            data = await get_lang('error_content_length_too_long') + db_data
        elif num == 45:
            data = await get_lang('cidr_error')
        elif num == 46:
            data = await get_lang('func_404_error')
            title = '404'
            return_code = 404
        elif num == 47:
            data = await get_lang('still_use_auth_error')
        elif num == 48:
            data = await get_lang('xss_data_include_error')
        elif num == 49:
            data = await get_lang('password_same_as_id_error')
        else:
            data = '???'

        if num == 5:
            if flask.request.path != '/skin_set':
                data += '<br>' + await get_lang('error_skin_set_old') + ' <a href="/skin_set">(' + await get_lang('go') + ')</a>'

            return await render_template(
                await get_lang('skin_set'),
                '' + \
                    '<div id="main_skin_set">' + \
                        '<h2>' + await get_lang('error') + '</h2>' + \
                        '<ul>' + \
                            '<li>' + data + '</a></li>' + \
                        '</ul>' + \
                    '</div>' + \
                '',
                0,
                [['change', await get_lang('user_setting')], ['change/skin_set/main', await get_lang('main_skin_set')]]
            )
        else:
            return await render_template(
                title,
                '' + \
                    '<h2>' + sub_title + '</h2>' + \
                    '<ul>' + \
                        '<li>' + data + '</li>' + \
                    '</ul>' + \
                '',
                0,
                0
            ), return_code
