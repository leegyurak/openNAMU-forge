# Init
import os
import sys
import smtplib
import datetime
import ipaddress

import email.mime.text
import email.utils
import email.header

if sys.version_info < (3, 10):
    raise RuntimeError('OpenNamu Forge requires Python 3.10 or newer.')

from opennamu_forge.infrastructure.logging import get_logger
from opennamu_forge.application.version import VERSION_INFO
from opennamu_forge.application.dto.settings import SettingKey
from opennamu_forge.application.ports.repositories import (
    AdminPort,
    BacklinkPort,
    BbsPort,
    DocumentMetaPort,
    HtmlFilterPort,
    HistoryPort,
    OtherSettingPort,
    RecentBlockPort,
    TopicPort,
    UserAgentDataPort,
    UserNoticePort,
    UserSettingPort,
    VotePort,
    WikiDocumentPort,
)
from opennamu_forge.application.services.settings_service import WikiSettingsService
from opennamu_forge.infrastructure.admin_repository import AdminRepository
from opennamu_forge.infrastructure.backlink_repository import BacklinkRepository
from opennamu_forge.infrastructure.bbs_repository import BbsRepository
from opennamu_forge.infrastructure.document_meta_repository import DocumentMetaRepository
from opennamu_forge.infrastructure.history_repository import HistoryRepository
from opennamu_forge.infrastructure.html_filter_repository import HtmlFilterRepository
from opennamu_forge.infrastructure.legacy_bootstrap import LegacyBootstrapAdapter
from opennamu_forge.infrastructure.recent_block_repository import RecentBlockRepository
from opennamu_forge.infrastructure.setting_repository import OtherSettingRepository
from opennamu_forge.infrastructure.topic_repository import TopicRepository
from opennamu_forge.infrastructure.user_agent_repository import UserAgentDataRepository
from opennamu_forge.infrastructure.user_notice_repository import UserNoticeRepository
from opennamu_forge.infrastructure.user_setting_repository import UserSettingRepository
from opennamu_forge.infrastructure.vote_repository import VoteRepository
from opennamu_forge.infrastructure.wiki_repository import WikiDocumentRepository

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
from .func_tool import *
from .func_render import class_do_render
from opennamu_forge.infrastructure.db_model import init_sqlmodel

from diff_match_patch import diff_match_patch

import werkzeug.routing
import werkzeug.debug

import flask
import asyncio
import nest_asyncio
import aiohttp

import requests
import psutil
from PIL import Image

try:
    import mysqlclient as pymysql
except:
    import pymysql

try:
    import psycopg
except ImportError:
    psycopg = None

if sys.version_info < (3, 6):
    import sha3

# Func
# Func-main
async def render_template(name, data, sub, menu, other = [], option = {}):
    other_set = {}
    other_set["name"] = name
    other_set["data"] = data
    other_set["sub"] = [sub] + other
    other_set["menu"] = menu
    other_set["option"] = {
        "path" : flask.request.path
    }

    for for_a in option:
        other_set["option"][for_a] = option[for_a]

    return await python_to_golang("post", other_set = other_set, path = "template")

global_lang_data = {}
global_some_set = {}

def do_db_set(db_set):
    for for_a in db_set:
        global_func_some_set_do('db_' + for_a, db_set[for_a])
        global_some_set_do('db_' + for_a, db_set[for_a])


def get_current_db_set():
    db_type = global_some_set_do("db_type")
    db_set = {
        "type": db_type,
        "name": global_some_set_do("db_name"),
    }

    if db_type == "mysql":
        db_set.update(
            {
                "mysql_host": global_some_set_do("db_mysql_host"),
                "mysql_user": global_some_set_do("db_mysql_user"),
                "mysql_pw": global_some_set_do("db_mysql_pw"),
                "mysql_port": global_some_set_do("db_mysql_port"),
            }
        )
    elif db_type == "postgresql":
        db_set.update(
            {
                "postgresql_host": global_some_set_do("db_postgresql_host"),
                "postgresql_user": global_some_set_do("db_postgresql_user"),
                "postgresql_pw": global_some_set_do("db_postgresql_pw"),
                "postgresql_port": global_some_set_do("db_postgresql_port"),
            }
        )

    return db_set


def get_other_setting_repository() -> OtherSettingPort:
    return OtherSettingRepository(get_current_db_set())


def get_admin_repository() -> AdminPort:
    return AdminRepository(get_current_db_set())


def get_html_filter_repository() -> HtmlFilterPort:
    return HtmlFilterRepository(get_current_db_set())


def get_bbs_repository() -> BbsPort:
    return BbsRepository(get_current_db_set())


def get_backlink_repository() -> BacklinkPort:
    return BacklinkRepository(get_current_db_set())


def get_recent_block_repository() -> RecentBlockPort:
    return RecentBlockRepository(get_current_db_set())


def get_legacy_bootstrap_repository() -> LegacyBootstrapAdapter:
    return LegacyBootstrapAdapter(get_current_db_set())


def get_wiki_settings_service() -> WikiSettingsService:
    return WikiSettingsService(get_other_setting_repository())


def get_wiki_document_repository() -> WikiDocumentPort:
    return WikiDocumentRepository(get_current_db_set())


def get_document_meta_repository() -> DocumentMetaPort:
    return DocumentMetaRepository(get_current_db_set())


def get_user_setting_repository() -> UserSettingPort:
    return UserSettingRepository(get_current_db_set())


def get_user_agent_repository() -> UserAgentDataPort:
    return UserAgentDataRepository(get_current_db_set())


def get_user_notice_repository() -> UserNoticePort:
    return UserNoticeRepository(get_current_db_set())


def get_vote_repository() -> VotePort:
    return VoteRepository(get_current_db_set())


def get_topic_repository() -> TopicPort:
    return TopicRepository(get_current_db_set())


def get_history_repository() -> HistoryPort:
    return HistoryRepository(get_current_db_set())

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

def global_some_set_do(set_name, data = None):
    global global_some_set

    if data != None:
        global_some_set[set_name] = data

    if set_name in global_some_set:
        return global_some_set[set_name]
    else:
        return None

async def python_to_golang(func_name, other_set = {}, path = ''):    
    headers = {}
    if flask.has_request_context():
        if "Cookie" in flask.request.headers:
            headers["Cookie"] = flask.request.headers["Cookie"]

        headers["X-Forwarded-For"] = ip_check()

    port_data = global_some_set_do("setup_golang_port")

    # print(func_name, other_set)

    if func_name == "same":
        async with aiohttp.ClientSession() as session:
            if flask.request.method == 'POST':
                form_data = flask.request.form.to_dict(flat = False)

                async with session.post('http://127.0.0.1:' + port_data + flask.request.path, data = form_data, headers = headers) as res:
                    data = await res.text()

                    return data
            else:
                async with session.get('http://127.0.0.1:' + port_data + flask.request.path, headers = headers) as res:
                    data = await res.text()

                    return data
    elif path != "":
        if func_name == "get":
            async with aiohttp.ClientSession() as session:
                async with session.get('http://127.0.0.1:' + port_data + "/api/" + path, headers = headers) as res:
                    data = await res.text()

                    return data
        elif func_name == "post":
            async with aiohttp.ClientSession() as session:
                async with session.post('http://127.0.0.1:' + port_data + "/api/" + path, data = json_dumps(other_set), headers = headers) as res:
                    data = await res.text()

                    return data
        elif func_name == "get_json":
            async with aiohttp.ClientSession() as session:
                async with session.get('http://127.0.0.1:' + port_data + "/api/" + path, headers = headers) as res:
                    data = await res.json()

                    return data
        else:
            async with aiohttp.ClientSession() as session:
                async with session.post('http://127.0.0.1:' + port_data + "/api/" + path, data = json_dumps(other_set), headers = headers) as res:
                    data = await res.json()

                    return data
    else:
        async with aiohttp.ClientSession() as session:
            async with session.post('http://127.0.0.1:' + port_data + '/compatible_api/' + func_name, data = json_dumps(other_set), headers = headers) as res:
                data = await res.json()

                if "response" in data and data["response"] == "error":
                    raise Exception(f"API returned error: {data}")
                else:
                    return data
                
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
def get_init_set_list(need = 'all'):
    init_set_list = {
        'host' : {
            'display' : 'Host',
            'require' : 'conv',
            'default' : '0.0.0.0'
        }, 'port' : {
            'display' : 'Port',
            'require' : 'conv',
            'default' : '3000'
        }, 'golang_port' : {
            'display' : 'Golang port',
            'require' : 'conv',
            'default' : '3001'
        }, 'language' : {
            'display' : 'Language',
            'require' : 'select',
            'default' : 'ko-KR',
            'list' : ['ko-KR', 'en-US']
        }, 'markup' : {
            'display' : 'Markup',
            'require' : 'select',
            'default' : 'namumark',
            'list' : ['namumark', 'namumark_beta', 'macromark', 'markdown', 'custom', 'raw']
        }, 'encode' : {
            'display' : 'Encryption method',
            'require' : 'select',
            'default' : 'sha3',
            'list' : ['sha3', 'sha3-salt', 'sha3-512', 'sha3-512-salt']
        }
    }
    
    if need == 'all':
        return init_set_list
    else:
        return init_set_list[need]
    
class get_db_connect:
    def __init__(self, db_type = '', init_mode = False):
        self.db_set = {}
        self.init_mode = init_mode

        for for_a in ("db_type", "db_name"):
            self.db_set[for_a] = global_some_set_do(for_a)

        if db_type != '':
            self.db_set['db_type'] = db_type

        if self.db_set['db_type'] == 'mysql':
            for for_a in ("db_mysql_host", "db_mysql_user", "db_mysql_pw", "db_mysql_port"):
                self.db_set[for_a] = global_some_set_do(for_a)
        elif self.db_set['db_type'] == 'postgresql':
            for for_a in ("db_postgresql_host", "db_postgresql_user", "db_postgresql_pw", "db_postgresql_port"):
                self.db_set[for_a] = global_some_set_do(for_a)
        
    def __enter__(self):
        if self.db_set['db_type'] == 'sqlite':
            self.conn = sqlite3.connect(
                self.db_set['db_name'] + '.db',
                check_same_thread = False,
                isolation_level = None
            )
        elif self.db_set['db_type'] == 'mysql':
            # try connect
            # print('Wait for DB connection...')

            self.conn = None
            try_cnt = 1
            max_try = 30
            while self.conn == None and try_cnt <= max_try:
                try:
                    if self.init_mode:
                        try:
                            self.conn = pymysql.connect(
                                host = self.db_set['db_mysql_host'],
                                user = self.db_set['db_mysql_user'],
                                password = self.db_set['db_mysql_pw'],
                                charset = 'utf8mb4',
                                port = int(self.db_set['db_mysql_port']),
                                autocommit = True,
                                db = self.db_set['db_name']
                            )
                        except pymysql.err.OperationalError:
                            self.conn = pymysql.connect(
                                host = self.db_set['db_mysql_host'],
                                user = self.db_set['db_mysql_user'],
                                password = self.db_set['db_mysql_pw'],
                                charset = 'utf8mb4',
                                port = int(self.db_set['db_mysql_port']),
                                autocommit = True
                            )
                    else:
                        self.conn = pymysql.connect(
                            host = self.db_set['db_mysql_host'],
                            user = self.db_set['db_mysql_user'],
                            password = self.db_set['db_mysql_pw'],
                            charset = 'utf8mb4',
                            port = int(self.db_set['db_mysql_port']),
                            autocommit = True,
                            db = self.db_set['db_name']
                        )
                except pymysql.err.OperationalError as err:
                    if try_cnt + 1 > max_try:
                        raise err
                finally:
                    if self.conn == None:
                        try_cnt += 1
                        
                        time.sleep(1)

            if self.conn == None:
                raise Exception("Unable to connect database")
        elif self.db_set['db_type'] == 'postgresql':
            if psycopg == None:
                raise ImportError('psycopg is required when NAMU_DB_TYPE=postgresql')

            self.conn = None
            try_cnt = 1
            max_try = 30
            while self.conn == None and try_cnt <= max_try:
                try:
                    self.conn = psycopg.connect(
                        host = self.db_set['db_postgresql_host'],
                        user = self.db_set['db_postgresql_user'],
                        password = self.db_set['db_postgresql_pw'],
                        port = int(self.db_set['db_postgresql_port']),
                        dbname = self.db_set['db_name'],
                        autocommit = True
                    )
                except psycopg.OperationalError as err:
                    if try_cnt + 1 > max_try:
                        raise err
                finally:
                    if self.conn == None:
                        try_cnt += 1

                        time.sleep(1)

            if self.conn == None:
                raise Exception("Unable to connect database")
        else:
            raise Exception("Unsupported database type: " + str(self.db_set['db_type']))

        # print('DB connected')

        return self.conn
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.conn.close()

# class get_whoosh_connect:

class class_check_json:
    def do_check_set_json(self):
        if os.getenv('NAMU_DB') or os.getenv('NAMU_DB_TYPE'):
            set_data = {}
            set_data['db'] = os.getenv('NAMU_DB') if os.getenv('NAMU_DB') else 'data'
            set_data['db_type'] = os.getenv('NAMU_DB_TYPE') if os.getenv('NAMU_DB_TYPE') else 'sqlite'
        else:
            if os.path.exists(os.path.join('data', 'set.json')):
                db_set_list = ['db', 'db_type']
                with open(os.path.join('data', 'set.json'), encoding = 'utf8') as file_data:
                    set_data = json_loads(file_data.read())

                for i in db_set_list:
                    if not i in set_data:
                        os.remove(os.path.join('data', 'set.json'))
                        break
            
            if not os.path.exists(os.path.join('data', 'set.json')):
                set_data = {}
                normal_db_type = ['sqlite', 'mysql', 'postgresql']

                print('DB type (' + normal_db_type[0] + ') [' + ', '.join(normal_db_type) + '] : ', end = '')
                try:
                    data_get = str(input())
                except EOFError:
                    logger.warning("Input is not available. You can set the environment variable NAMU_DB_TYPE instead.")
                    logger.warning("No input detected. Using default value.")
                    data_get = ''

                if data_get == 'postgres':
                    data_get = 'postgresql'

                if data_get == '' or not data_get in normal_db_type:
                    set_data['db_type'] = 'sqlite'
                else:
                    set_data['db_type'] = data_get

                all_src = []
                if set_data['db_type'] == 'sqlite':
                    for i_data in os.listdir("."):
                        f_src = re.search(r"(.+)\.db$", i_data)
                        if f_src:
                            all_src += [f_src.group(1)]

                print('DB name (data) [' + ', '.join(all_src) + '] : ', end = '')

                data_get = str(input())
                if data_get == '':
                    set_data['db'] = 'data'
                else:
                    set_data['db'] = data_get

                with open(os.path.join('data', 'set.json'), 'w', encoding = 'utf8') as f:
                    f.write(json_dumps(set_data))

        if set_data['db_type'] == 'postgres':
            set_data['db_type'] = 'postgresql'

        logger.info('DB name : %s', set_data['db'])
        logger.info('DB type : %s', set_data['db_type'])
        
        data_db_set = {}
        data_db_set['name'] = set_data['db']
        data_db_set['type'] = set_data['db_type']

        return data_db_set

    def do_check_mysql_json(self, data_db_set):
        
        def do_check_mysql_env():
            env_keys = ['NAMU_DB_HOST', 'NAMU_DB_PORT', 'NAMU_DB_USER', 'NAMU_DB_PASSWORD']
            vaild = False
            for key in env_keys:
                if os.getenv(key):
                    vaild = True
                    break
            return vaild
        
        if do_check_mysql_env():
            # ['user', 'password', 'host', 'port']
            set_data_mysql = {}
            set_data_mysql['host'] = os.getenv('NAMU_DB_HOST') if os.getenv('NAMU_DB_HOST') else '127.0.0.1'
            set_data_mysql['port'] = os.getenv('NAMU_DB_PORT') if os.getenv('NAMU_DB_PORT') else 3306

            if not os.getenv('NAMU_DB_USER'):
                raise Exception('Error : NAMU_DB_USER env not set')
            else: 
                set_data_mysql['user'] = os.getenv('NAMU_DB_USER')
            if not os.getenv('NAMU_DB_PASSWORD'):
                raise Exception('Error : NAMU_DB_PASSWORD env not set')
            else:
                set_data_mysql['password'] = os.getenv('NAMU_DB_PASSWORD')
        elif os.path.exists(os.path.join('data', 'mysql.json')):
            db_set_list = ['user', 'password', 'host', 'port']
            with open(os.path.join('data', 'mysql.json'), encoding = 'utf8') as file_data:
                set_data = json_loads(file_data.read())

            for i in db_set_list:
                if not i in set_data:
                    os.remove(os.path.join('data', 'mysql.json'))
                    
                    break

            set_data_mysql = set_data
        elif not os.path.exists(os.path.join('data', 'mysql.json')):
            set_data_mysql = {}

            print('DB user ID : ', end = '')
            set_data_mysql['user'] = str(input())

            print('DB password : ', end = '')
            set_data_mysql['password'] = str(input())

            print('DB host (127.0.0.1) : ', end = '')
            set_data_mysql['host'] = str(input())
            if set_data_mysql['host'] == '':
                set_data_mysql['host'] = '127.0.0.1'

            print('DB port (3306) : ', end = '')
            set_data_mysql['port'] = str(input())
            if set_data_mysql['port'] == '':
                set_data_mysql['port'] = '3306'

            with open(os.path.join('data', 'mysql.json'), 'w', encoding = 'utf8') as f:
                f.write(json_dumps(set_data_mysql))

        data_db_set['mysql_user'] = set_data_mysql['user']
        data_db_set['mysql_pw'] = set_data_mysql['password']
        if 'host' in set_data_mysql:
            data_db_set['mysql_host'] = set_data_mysql['host']
        else:
            data_db_set['mysql_host'] = '127.0.0.1'

        if 'port' in set_data_mysql:
            data_db_set['mysql_port'] = set_data_mysql['port']
        else:
            data_db_set['mysql_port'] = '3306'

        return data_db_set

    def do_check_postgresql_json(self, data_db_set):

        def do_check_postgresql_env():
            env_keys = ['NAMU_DB_HOST', 'NAMU_DB_PORT', 'NAMU_DB_USER', 'NAMU_DB_PASSWORD']
            vaild = False
            for key in env_keys:
                if os.getenv(key):
                    vaild = True
                    break
            return vaild

        if do_check_postgresql_env():
            set_data_postgresql = {}
            set_data_postgresql['host'] = os.getenv('NAMU_DB_HOST') if os.getenv('NAMU_DB_HOST') else '127.0.0.1'
            set_data_postgresql['port'] = os.getenv('NAMU_DB_PORT') if os.getenv('NAMU_DB_PORT') else 5432

            if not os.getenv('NAMU_DB_USER'):
                raise Exception('Error : NAMU_DB_USER env not set')
            else:
                set_data_postgresql['user'] = os.getenv('NAMU_DB_USER')
            if not os.getenv('NAMU_DB_PASSWORD'):
                raise Exception('Error : NAMU_DB_PASSWORD env not set')
            else:
                set_data_postgresql['password'] = os.getenv('NAMU_DB_PASSWORD')
        elif os.path.exists(os.path.join('data', 'postgresql.json')):
            db_set_list = ['user', 'password', 'host', 'port']
            with open(os.path.join('data', 'postgresql.json'), encoding = 'utf8') as file_data:
                set_data = json_loads(file_data.read())

            for i in db_set_list:
                if not i in set_data:
                    os.remove(os.path.join('data', 'postgresql.json'))

                    break

            set_data_postgresql = set_data
        elif not os.path.exists(os.path.join('data', 'postgresql.json')):
            set_data_postgresql = {}

            print('DB user ID : ', end = '')
            set_data_postgresql['user'] = str(input())

            print('DB password : ', end = '')
            set_data_postgresql['password'] = str(input())

            print('DB host (127.0.0.1) : ', end = '')
            set_data_postgresql['host'] = str(input())
            if set_data_postgresql['host'] == '':
                set_data_postgresql['host'] = '127.0.0.1'

            print('DB port (5432) : ', end = '')
            set_data_postgresql['port'] = str(input())
            if set_data_postgresql['port'] == '':
                set_data_postgresql['port'] = '5432'

            with open(os.path.join('data', 'postgresql.json'), 'w', encoding = 'utf8') as f:
                f.write(json_dumps(set_data_postgresql))

        data_db_set['postgresql_user'] = set_data_postgresql['user']
        data_db_set['postgresql_pw'] = set_data_postgresql['password']
        if 'host' in set_data_postgresql:
            data_db_set['postgresql_host'] = set_data_postgresql['host']
        else:
            data_db_set['postgresql_host'] = '127.0.0.1'

        if 'port' in set_data_postgresql:
            data_db_set['postgresql_port'] = set_data_postgresql['port']
        else:
            data_db_set['postgresql_port'] = '5432'

        return data_db_set
    
    def __init__(self):
        self.data_db_set = {}
            
    def __new__(cls):
        instance = super().__new__(cls)

        cls.data_db_set = instance.do_check_set_json()
        if cls.data_db_set['type'] == 'mysql':
            cls.data_db_set = instance.do_check_mysql_json(cls.data_db_set)
        elif cls.data_db_set['type'] == 'postgresql':
            cls.data_db_set = instance.do_check_postgresql_json(cls.data_db_set)
        
        return cls.data_db_set

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

async def update(conn, ver_num, set_data):
    legacy_bootstrap = get_legacy_bootstrap_repository()
    html_filters = get_html_filter_repository()
    settings = get_other_setting_repository()
    user_settings = get_user_setting_repository()
    document_meta = get_document_meta_repository()
    wiki_documents = get_wiki_document_repository()
    history = get_history_repository()

    # 업데이트 하위 호환 유지 함수
    if ver_num < 3160027:
        logger.info('Add init set')
        set_init(conn)

        ver_num = 3160027

    if ver_num < 3170002:
        if not html_filters.list_by_kind('extension'):
            for i in ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg']:
                html_filters.upsert(i, 'extension')
        
        ver_num = 3170002

    if ver_num < 3170400:
        for i in legacy_bootstrap.list_old_topic_first_rows():
            legacy_bootstrap.update_old_topic_code(i[0], i[1], i[2])

        ver_num = 3170400

    if ver_num < 3171800:
        change_rec = settings.get('recaptcha')
        if change_rec != '':
            new_rec = re.search(r'data-sitekey="([^"]+)"', change_rec)
            if new_rec:
                settings.upsert('recaptcha', new_rec.group(1))
            else:
                settings.upsert('recaptcha', '')
                settings.upsert('sec_re', '')

        ver_num = 3171800
    
    if ver_num < 3172800 and set_data['type'] == 'mysql':
        get_data_mysql = json_loads(open('data/mysql.json', encoding = 'utf8').read())
        
        with open('data/mysql.json', 'w') as f:
            f.write('{ "user" : "' + get_data_mysql['user'] + '", "password" : "' + get_data_mysql['password'] + '", "host" : "127.0.0.1" }')

        ver_num = 3172800

    if ver_num < 3183603:
        for i in legacy_bootstrap.list_legacy_ban_regex_blocks():
            legacy_bootstrap.convert_legacy_ban_regex_block(i, '^' + i.replace('.', '\\.'))

        for i in legacy_bootstrap.list_recent_block_regex_blocks():
            legacy_bootstrap.convert_recent_block_regex_block(i, '^' + i.replace('.', '\\.'))
        
        ver_num = 3183603

    if ver_num < 3190201:
        today_time = get_time()

        for i in legacy_bootstrap.list_legacy_bans():
            get_recent_block_repository().add_record(i[0], i[1], today_time, '', i[2], i[3], '1', i[4])
        
        ver_num = 3190201

    if ver_num < 3191301:
        data_list = legacy_bootstrap.list_recent_history_rows_excluding_user()
        for get_data in data_list:
            history.add_recent_change(get_data[1], get_data[0], get_data[2], 'normal')
        
        ver_num = 3191301

    if ver_num < 3202400:
        get_data = settings.get('update')
        if get_data == 'master':
            settings.upsert('update', 'beta')
        
        ver_num = 3202400

    if ver_num < 3202600:
        for i in legacy_bootstrap.list_legacy_filters():
            html_filters.upsert(i[0], 'regex_filter', plus=i[1], plus_t=i[2])

        for i in legacy_bootstrap.list_legacy_interwiki():
            html_filters.upsert(i[0], 'inter_wiki', plus=i[1], plus_t=i[2])
        
        ver_num = 3202600

    if ver_num < 3203400:
        for i in legacy_bootstrap.list_legacy_custom_css():
            user_settings.add(re.sub(r' \(head\)$', '', i[0]), 'custom_css', i[1])
        
        ver_num = 3203400

    if ver_num < 3205500:
        for i in legacy_bootstrap.list_legacy_acl_rows():
            document_meta.upsert_acl(i[0], 'decu', i[1])
            document_meta.upsert_acl(i[0], 'dis', i[2])
            document_meta.upsert_acl(i[0], 'view', i[3])
            document_meta.upsert_acl(i[0], 'why', i[4])
        
        ver_num = 3205500

    if ver_num < 3300101:
        # 캐시 초기화
        legacy_bootstrap.clear_legacy_cache()
        
        ver_num = 3300101
    
    if ver_num < 3300301:
        # regex_filter 오류 해결
        legacy_bootstrap.delete_null_regex_filters()
        
        ver_num = 3300301
        
    if ver_num < 3302302:
        # user이랑 user_set 테이블의 통합
        for i in legacy_bootstrap.list_legacy_users():
            user_settings.add(i[0], 'pw', i[1])
            user_settings.add(i[0], 'acl', i[2])
            user_settings.add(i[0], 'date', i[3])
            user_settings.add(i[0], 'encode', i[4])
        
        ver_num = 3302302
            
    if ver_num < 3400101:
        # user_set이랑 user_application 테이블의 통합
        for i in legacy_bootstrap.list_legacy_user_applications():
            sql_data = {}
            sql_data['id'] = i[0]
            sql_data['pw'] = i[1]
            sql_data['date'] = i[2]
            sql_data['encode'] = i[3]
            sql_data['question'] = i[4]
            sql_data['answer'] = i[5]
            sql_data['ip'] = i[6]
            sql_data['ua'] = i[7]
            sql_data['email'] = i[8]
            
            user_settings.add(i[0], 'application', json_dumps(sql_data))
        
        ver_num = 3400101
    
    if ver_num < 3500105:
        legacy_bootstrap.delete_file_admin_decu_acl()
        
        ver_num = 3500105
        
    if ver_num < 3500106:
        db_data = settings.get('domain')
        if db_data != '':
            db_data = re.match(r'[^/]+\/\/([^/]+)', db_data)
            if db_data:
                db_data = db_data.group(1)
                settings.upsert('domain', db_data)
            else:
                settings.upsert('domain', '')
        
        ver_num = 3500106

    if ver_num < 3500107:
        legacy_bootstrap.normalize_nulls(get_db_table_list())
        
        ver_num = 3500107
                
    if ver_num < 3500113:
        legacy_bootstrap.normalize_nulls(get_db_table_list())
        
        ver_num = 3500113

    if ver_num < 3500114:
        legacy_bootstrap.clear_legacy_alarm()
        
        ver_num = 3500114

    if ver_num < 3500354:
        db_data = settings.get('robot')
        if db_data != '':
            robot_default = '' + \
                'User-agent: *\n' + \
                'Disallow: /\n' + \
                'Allow: /$\n' + \
                'Allow: /image/\n' + \
                'Allow: /views/\n' + \
                'Allow: /w/' + \
            ''
            if db_data == robot_default:
                settings.upsert('robot_default', 'on')
        
        ver_num = 3500354

    if ver_num < 3500355:
        # other coverage 오류 해결
        legacy_bootstrap.normalize_other_coverage()
        
        ver_num = 3500355

    if ver_num < 3500358:
        legacy_bootstrap.rebuild_history_index()
        
        ver_num = 3500358

    if ver_num < 3500360:
        # 마지막 편집 따로 기록하도록
        # create_data['data_set'] = ['doc_name', 'doc_rev', 'set_name', 'set_data']
        logger.info("Update 3500360...")

        legacy_bootstrap.clear_last_edit_meta()

        for for_a in wiki_documents.list_titles():
            db_data_2 = legacy_bootstrap.latest_history_date_by_title(for_a)
            if db_data_2:
                document_meta.upsert(for_a, 'last_edit', db_data_2)

        legacy_bootstrap.delete_file_admin_decu_acl()

        logger.info("Update 3500360 complete")
        ver_num = 3500360

    if ver_num < 3500361:
        for db_data in legacy_bootstrap.list_email_user_ids():
            if ip_or_user(db_data) == 1:
                user_settings.delete(db_data, 'email')
        
        ver_num = 3500361

    # create_data['history'] = ['id', 'title', 'data', 'date', 'ip', 'send', 'leng', 'hide', 'type']
    # create_data['rc'] = ['id', 'title', 'date', 'type']
    if ver_num == 3500362:
        legacy_bootstrap.rebuild_history_index()

    if ver_num < 3500365:
        legacy_bootstrap.normalize_backlink_data()
        
        ver_num = 3500365

    if ver_num < 3500371:
        legacy_bootstrap.clear_user_notices()
        user_alarm_count = {}

        for db_data in legacy_bootstrap.list_legacy_alarms():
            if db_data[0] in user_alarm_count:
                user_alarm_count[db_data[0]] += 1
            else:
                user_alarm_count[db_data[0]] = 1

            legacy_bootstrap.add_user_notice(str(user_alarm_count[db_data[0]]), db_data[0], db_data[1], db_data[2])
        
        ver_num = 3500371

    if ver_num < 3500372:
        # ID 글자 확인 호환용
        html_filters.upsert(r'(?:[^A-Za-zㄱ-ㅣ가-힣0-9])', 'name')
        
        ver_num = 3500372

    if ver_num < 3500373:
        select_data = {}

        for db_data in legacy_bootstrap.list_application_settings():
            select_data[db_data[1]] = db_data

        legacy_bootstrap.delete_application_settings()
        
        for db_data in select_data:
            user_settings.add(select_data[db_data][1], select_data[db_data][0], select_data[db_data][2])
        
        ver_num = 3500373

    if ver_num < 3500374:
        # ban 오류 해결
        legacy_bootstrap.normalize_recent_block_nullable_columns()
        
        ver_num = 3500374

    if ver_num < 3500375:
        for for_a in legacy_bootstrap.list_legacy_scan_rows():
            type_data = 'watchlist' if for_a[1] == '' else 'star_doc'
            user_settings.add(for_a[2], type_data, for_a[0])
        
        ver_num = 3500375

    if ver_num < 3500376:
        for for_a in legacy_bootstrap.list_edit_request_meta():
            get_data = history.latest_revision_id(for_a[0])
            if get_data and (int(get_data) + 1) == int(for_a[1]):
                document_meta.upsert(for_a[0], 'edit_request_doing', '1', doc_rev=for_a[1])
        
        ver_num = 3500376

    if ver_num < 3500377 and set_data['type'] == 'sqlite':
        legacy_bootstrap.set_sqlite_delete_journal(conn)
        
        ver_num = 3500377

    if ver_num < 3500378:
        for for_a in legacy_bootstrap.list_special_titles():
            mode = ''
            if re.search('^user:', for_a):
                mode = 'user'
            elif re.search('^file:', for_a):
                mode = 'file'
            elif re.search('^category:', for_a):
                mode = 'category'
            
            document_meta.upsert(for_a, 'doc_type', mode)
        
        ver_num = 3500378

    if ver_num < 3500379:
        for for_a in legacy_bootstrap.list_document_meta_names_with_revision_marker():
            data_set_exist = ''
            
            if not wiki_documents.exists_title(for_a):
                data_set_exist = 'not_exist'

            document_meta.update_revision_marker(for_a, data_set_exist)
        
        ver_num = 3500379

    if ver_num < 20240513:
        legacy_bootstrap.normalize_user_title_checkmark()
        
        ver_num = 20240513

    if ver_num < 20240732:
        for for_a in legacy_bootstrap.list_owner_acl_group_names():
            for for_b in legacy_bootstrap.list_user_ids_by_acl(for_a):
                lang_name = 'en-US'
                if lang_name == 'ko-KR':
                    logger.warning('메인 ACL이 권한으로 개편되면서 기존 설정 값이 날라갔으니 권한으로 재설정 해주세요.')
                else:
                    logger.warning('As the main ACL has been reorganized into the auth, the existing setting values have been lost, so please reset it to the auth.')
        
        ver_num = 20240732

    logger.info('Update completed')

def set_init_always(conn, ver_num, run_mode):
    settings = get_other_setting_repository()
    admins = get_admin_repository()

    # 버전 기입
    settings.upsert('ver', ver_num)
    
    # 기본 권한 그룹 설정
    admins.set_group_acls('owner', ('owner',))

    if 'user' not in admins.list_group_names():
        admins.set_group_acls('user', ('user',))

    if 'ip' not in admins.list_group_names():
        admins.set_group_acls('ip', ('ip',))

    if 'ban' not in admins.list_group_names():
        admins.set_group_acls('ban', ('view',))

    # 문서 댓글용 게시판 생성
    bbs_num = '0'
    bbs_name = 'document_comment'
    bbs_type = 'comment'
    bbs = get_bbs_repository()

    if bbs.get_setting(bbs_num, 'bbs_name') == '':
        bbs.add_setting(bbs_num, 'bbs_name', bbs_name)

    if bbs.get_setting(bbs_num, 'bbs_type') == '':
        bbs.add_setting(bbs_num, 'bbs_type', bbs_type)

    # 이미지 폴더 없으면 생성
    if not os.path.exists(load_image_url(conn)):
        os.makedirs(load_image_url(conn))

    # 비밀키 없으면 생성
    if not settings.exists('key'):
        settings.upsert('key', load_random_key())

    # 솔트키 없으면 생성
    if not settings.exists('salt_key'):
        settings.upsert('salt_key', load_random_key(4))

    # 문서 전체 갯수 없으면 생성
    if not settings.exists('count_all_title'):
        settings.upsert('count_all_title', '0')
        
    # 위키 접근 비밀번호 있으면 temp DB로 넘겨줌
    db_data = settings.get('wiki_access_password_need')
    if db_data != '':
        wiki_access_password = settings.get('wiki_access_password')
        if wiki_access_password != '':
            global_some_set_do("wiki_access_password", wiki_access_password)

    db_data = settings.get('load_ip_select')
    if db_data != '':
        global_func_some_set_do("load_ip_select", db_data)

    # OS마다 실행 파일 설정
    exe_type = linux_exe_chmod()
    if platform.system() == 'Linux' or platform.system() == 'Darwin':
        os.system('chmod +x ./bin/' + exe_type)

def linux_exe_chmod():
    exe_type = ''
    if platform.system() == 'Linux':
        if platform.machine() in ["AMD64", "x86_64"]:
            exe_type = 'main.amd64.bin'
        else:
            exe_type = 'main.arm64.bin'
    elif platform.system() == 'Darwin':
        exe_type = 'main.mac.arm64.bin'
    else:
        if platform.machine() in ["AMD64", "x86_64"]:
            exe_type = 'main.amd64.exe'
        else:
            exe_type = 'main.arm64.exe'

    return exe_type

def set_init(conn):
    html_filters = get_html_filter_repository()
    settings = get_other_setting_repository()

    # 초기값 설정 함수    
    if not html_filters.list_by_kind('email'):
        for i in ['naver.com', 'gmail.com', 'daum.net', 'kakao.com']:
            html_filters.upsert(i, 'email')

    if not html_filters.list_by_kind('extension'):
        for i in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
            html_filters.upsert(i, 'extension')

    if not settings.list_name_data_by_names(('smtp_server', 'smtp_port', 'smtp_security')):
        for i in [['smtp_server', 'smtp.gmail.com'], ['smtp_port', '587'], ['smtp_security', 'starttls']]:
            settings.upsert(i[0], i[1])

    html_filters.upsert(r'(?:[^A-Za-zㄱ-ㅣ가-힣0-9])', 'name')

# Func-simple
## Func-simple-without_DB
def get_default_admin_group():
    return ['owner', 'user', 'ip', 'ban']

def get_default_robots_txt(conn):
    data = '' + \
        'User-agent: *\n' + \
        'Disallow: /\n' + \
        'Allow: /$\n' + \
        'Allow: /w/\n' + \
        'Allow: /bbs/w/\n' + \
        'Allow: /sitemap.xml$\n' + \
        'Allow: /sitemap_*.xml$' + \
    ''

    if os.path.exists('sitemap.xml'):
        data += '' + \
            '\n' + \
            'Sitemap: ' + load_domain(conn, 'full') + '/sitemap.xml' + \
        ''

    return data

def load_random_key(long = 128):
    return ''.join(random.choice("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(long))

async def http_warning():
    return '''
        <div id="opennamu_forge_http_warning_text"></div>
        <span style="display: none;" id="opennamu_forge_http_warning_text_lang">''' + await get_lang('http_warning') + '''</span>
    '''

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

def leng_check(A, B):
    # B -> new
    # A -> old
    return '0' if A == B else (('-' + str(A - B)) if A > B else ('+' + str(B - A)))

def number_check(data, f = 0):
    try:
        float(data) if f == 1 else int(data)
        return data
    except:
        return '1'
    
def redirect(conn, data = '/'):
    return flask.redirect(load_domain(conn, 'full') + data)
    
# Golang 의존
async def get_acl_list(type_data = 'normal'):
    if type_data == 'user':
        type_data = 'user_document'

    other_set = {}
    other_set['type'] = type_data

    data = await python_to_golang('api_list_acl', other_set)

    return data["data"]

## Func-simple-with_DB
async def get_user_title_list(conn, ip = ''):
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

    if await acl_check(tool = 'all_admin_auth') != 1:
        user_title['✅'] = '✅ admin'
    
    return user_title
    
def load_image_url(conn):
    image_where = get_other_setting_repository().get('image_where', default=os.path.join('data', 'images'))
    
    return image_where

def load_domain(conn, data_type = 'normal'):
    domain = ''
    try:
        sys_host = flask.request.host
    except:
        sys_host = ''
    
    if data_type == 'full':
        settings = get_other_setting_repository()
        domain += settings.get('http_select') or 'http'
        domain += '://'

        domain += settings.get('domain') or sys_host
    else:
        domain += get_other_setting_repository().get('domain') or sys_host

    return domain

def get_tool_js_safe(data):
    data = data.replace('\n', '\\\\n')
    data = data.replace('\\', '\\\\')
    data = data.replace("'", "\\'")
    data = data.replace('"', '\\"')

    return data

async def edit_button(conn):
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

async def ip_warning(conn):
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
def pw_encode(conn, data, db_data_encode = ''):
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

def pw_check(conn, data, data2, type_d = 'no', id_d = ''):
    load_set_data = get_other_setting_repository().get('encode') or 'sha3'
    
    set_data = load_set_data
    if type_d != 'no':
        set_data = 'sha3' if type_d == '' else type_d

    re_data = 1 if pw_encode(conn, data, set_data) == data2 else 0
    if load_set_data != set_data and re_data == 1 and id_d != '':
        user_settings = get_user_setting_repository()
        user_settings.upsert(id_d, 'pw', pw_encode(conn, data))
        user_settings.upsert(id_d, 'encode', load_set_data)

    return re_data
        
# Func-skin
async def get_lang(data, safe = 0):
    if data in global_lang_data:
        if safe == 1:
            return html.unescape(global_lang_data[data])
        else:
            return global_lang_data[data]
    else:
        lang = json_loads(open(os.path.join('lang', 'en-US.json'), encoding = 'utf-8').read())

        other_set = {}
        other_set["data"] = ' '.join([title for title in lang if title[0] != '_'])
        other_set["legacy"] = ""
        other_set["safe"] = ""

        res = await python_to_golang('api_func_language', other_set)
        if res['response'] == 'ok':
            for load_data in res['data']:
                global_lang_data[load_data] = res['data'][load_data]

        if data in global_lang_data:
            if safe == 1:
                return html.unescape(global_lang_data[data])
            else:
                return global_lang_data[data]
        else:
            return data + ' (M)'

# 하위 호환용
def load_lang(data, safe = 0):
    try:
        loop = asyncio.get_running_loop()
        if loop.is_running():
            nest_asyncio.apply()
            return loop.run_until_complete(get_lang(data, safe))
    except RuntimeError:
        return asyncio.run(get_lang(data, safe))

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
    
def cache_v():
    return '.cache_v289'

def cut_100(data):
    return ''

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
async def render_set(conn, doc_name = '', doc_data = '', data_type = 'view', markup = '', parameter = {}):
    # data_type in ['view', 'from', 'thread', 'api_view', 'api_thread', 'api_include', 'backlink']
    # data_type을 list 형식으로 개편 필요할 듯

    return_type = True
    if data_type in ['api_from', 'api_view', 'api_thread', 'api_include']:
        return_type = False

    if await acl_check(doc_name, 'render') == 1:
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
        conn,
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

    font_size_set_data = get_main_skin_set(conn, flask.session, 'main_css_font_size', ip)
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

    table_set_data = get_main_skin_set(conn, flask.session, 'main_css_table_scroll', ip)
    if table_set_data == 'on':
        get_class_render[0] = '<style>.table_safe { overflow-x: scroll; white-space: nowrap; }</style>' + get_class_render[0]

    joke_set_data = get_main_skin_set(conn, flask.session, 'main_css_view_joke', ip)
    if joke_set_data == 'off':
        get_class_render[0] = '<style>.opennamu_forge_joke { display: none; }</style>' + get_class_render[0]

    math_set_data = get_main_skin_set(conn, flask.session, 'main_css_math_scroll', ip)
    if math_set_data == 'on':
        get_class_render[0] = '<style>.katex .base { overflow-x: scroll; }</style>' + get_class_render[0]

    transparent_set_data = get_main_skin_set(conn, flask.session, 'main_css_table_transparent', ip)
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
        
async def render_simple_set(data):
    # without_DB

    toc_data = ''
    toc_regex = r'<h([1-6])>([^<>]+)<\/h[1-6]>'
    toc_search_data = re.findall(toc_regex,  data)
    heading_stack = [0, 0, 0, 0, 0, 0]

    if toc_search_data:
        toc_data += '''
            <div class="opennamu_forge_TOC" id="toc">
                <span class="opennamu_forge_TOC_title">''' + await get_lang('toc') + '''</span>
                <br>
        '''
    
    for toc_search_in in toc_search_data:
        heading_level = int(toc_search_in[0])
        heading_level_str = str(heading_level)

        heading_stack[heading_level - 1] += 1
        for for_a in range(heading_level, 6):
            heading_stack[for_a] = 0
        
        heading_stack_str = ''.join([str(for_a) + '.' if for_a != 0 else '' for for_a in heading_stack])
        heading_stack_str = re.sub(r'\.$', '', heading_stack_str)
    
        toc_data += '''
            <br>
            <span class="opennamu_forge_TOC_list">
                ''' + ('<span style="margin-left: 10px;"></span>' * (heading_stack_str.count('.'))) + '''
                <a href="#s-''' + heading_stack_str + '''">''' + heading_stack_str + '''.</a>
                ''' + toc_search_in[1] + '''
            </span>
        '''
        
        data = re.sub(toc_regex, '<h' + toc_search_in[0] + ' id="s-' + heading_stack_str + '"><a href="#toc">' + heading_stack_str + '.</a> ' + toc_search_in[1] + '</h' + toc_search_in[0] + '>', data, 1)
        
    if toc_data != '':
        toc_data += '</div>'
        
    footnote_data = ''
    footnote_regex = r'<sup>((?:(?!<sup>|<\/sup>).)+)<\/sup>'
    footnote_search_data = re.findall(footnote_regex, data)
    footnote_count = 1
    if footnote_search_data:
        footnote_data += '<div class="opennamu_forge_footnote">'
    
    for footnote_search in footnote_search_data:
        footnote_count_str = str(footnote_count)
        
        if footnote_count != 1:
            footnote_data += '<br>'
    
        footnote_data += '<a id="fn-' + footnote_count_str + '" href="#rfn-' + footnote_count_str + '">(' + footnote_count_str + ')</a> ' + footnote_search
        data = re.sub(footnote_regex, '<sup id="rfn-' + footnote_count_str + '"><a href="#fn-' + footnote_count_str + '">(' + footnote_count_str + ')</a></sup>', data, 1)
        
        footnote_count += 1
        
    if footnote_data != '':
        footnote_data += '</div>'
        
    data = toc_data + data + footnote_data

    return data

# Func-request
async def send_email(conn, who, title, data):
    rep_data = dict(get_other_setting_repository().list_name_data_by_names((
        'smtp_email',
        'smtp_pass',
        'smtp_server',
        'smtp_port',
        'smtp_security',
    )))

    smtp_email = rep_data.get('smtp_email', '')
    smtp_pass = rep_data.get('smtp_pass', '')
    smtp_server = rep_data.get('smtp_server', '')
    smtp_security = rep_data.get('smtp_security', '')
    smtp_port = rep_data.get('smtp_port', '')
    smtp = ''
    
    smtp_port = int(number_check(smtp_port))
    if smtp_security == 'plain':
        smtp = smtplib.SMTP(smtp_server, smtp_port)
    elif smtp_security == 'starttls':
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.starttls()
    else:
        # if smtp_security == 'tls':
        smtp = smtplib.SMTP_SSL(smtp_server, smtp_port)
        
    domain = load_domain(conn)
    wiki_name = (await wiki_set())[0]
    
    msg = email.mime.text.MIMEText(data)

    msg['Subject'] = title
    msg['From'] = wiki_name + ' <noreply@' + domain + '>'
    msg['To'] = who

    try:
        smtp.login(smtp_email, smtp_pass)
        
        smtp.sendmail('openNAMU@' + domain, who, msg.as_string())
        smtp.quit()

        return 1
    except Exception:
        logger.exception('Error : email send error')

        return 0

async def captcha_get(conn):
    data = ''
    
    if await acl_check('', 'recaptcha_five_pass') == 0 and 'recapcha_pass' in flask.session and flask.session['recapcha_pass'] > 0:
        pass
    elif await acl_check('', 'recaptcha') == 1:
        settings = get_other_setting_repository()
        recaptcha = settings.get('recaptcha')
        sec_re = settings.get('sec_re')
        rec_ver = settings.get('recaptcha_ver')
        if recaptcha != '' and sec_re != '':
            if rec_ver == '':
                data += '' + \
                    '<script defer src="https://www.google.com/recaptcha/api.js"></script>' + \
                    '<div class="g-recaptcha" data-sitekey="' + recaptcha + '"></div>' + \
                    '<hr class="main_hr">' + \
                ''
            elif rec_ver == 'v3':
                data += '' + \
                    '<script defer src="https://www.google.com/recaptcha/api.js?render=' + recaptcha + '"></script>' + \
                    '<input class="__ON_INPUT__" type="hidden" id="g-recaptcha" name="g-recaptcha">' + \
                    '<script type="text/javascript">' + \
                        'document.addEventListener(\'DOMContentLoaded\', function () {' + \
                            'grecaptcha.ready(function() {' + \
                                'grecaptcha.execute(\'' + recaptcha + '\', {action: \'homepage\'}).then(function(token) {' + \
                                    'document.getElementById(\'g-recaptcha\').value = token;' + \
                                '});' + \
                            '});' + \
                        '});' + \
                    '</script>' + \
                ''
            elif rec_ver == 'cf':
                data += '' + \
                    '<script defer src="https://challenges.cloudflare.com/turnstile/v0/api.js?compat=recaptcha"></script>' + \
                    '<div class="g-recaptcha" data-sitekey="' + recaptcha + '"></div>' + \
                    '<hr class="main_hr">' + \
                ''
            else:
                # rec_ver == 'h'
                data += '''
                    <script defer src="https://js.hcaptcha.com/1/api.js"></script>
                    <div class="h-captcha" data-sitekey="''' + recaptcha + '''"></div>
                    <hr class="main_hr">
                '''

    return data

async def captcha_post(conn, re_data):
    if await acl_check('', 'recaptcha_five_pass') == 0 and 'recapcha_pass' in flask.session and flask.session['recapcha_pass'] > 0:
        pass
    elif await acl_check('', 'recaptcha') == 1:
        settings = get_other_setting_repository()
        sec_re = settings.get('sec_re')
        rec_ver = settings.get('recaptcha_ver')
        if await captcha_get(conn) != '':
            url = ''
            if rec_ver in ('', 'v3'):
                url = 'https://www.google.com/recaptcha/api/siteverify'
            elif rec_ver == 'cf':
                url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'
            else:
                # rec_ver == 'h'
                url = 'https://hcaptcha.com/siteverify'

            async with aiohttp.ClientSession() as session:
                async with session.post(url, data = {
                    "secret": sec_re,
                    "response": re_data
                }) as res:
                    if res.status == 200:
                        json_data = await res.json()
                        if json_data['success'] != True:
                            return 1

    if 'recapcha_pass' in flask.session:
        if flask.session['recapcha_pass'] > 0:
            flask.session['recapcha_pass'] -= 1
        else:
            flask.session['recapcha_pass'] = 5
    else:
        flask.session['recapcha_pass'] = 5

    return 0

# Func-user
def do_user_name_check(conn, user_name):
    html_filters = get_html_filter_repository()
    user_settings = get_user_setting_repository()

    # XSS 필터
    if html.escape(user_name) != user_name:
        return 1

    # IP와 혼동 방지 
    if ip_or_user(user_name) == 1:
        return 1
    
    # 슬래시 불가능
    if user_name.find('/') != -1:
        return 1

    # ID 필터
    set_d = html_filters.list_by_kind('name')
    for i in set_d:
        check_r = re.compile(i.html, re.I)
        if check_r.search(user_name):
            return 1

    # ID 길이 제한 (128글자)
    if len(user_name) > 128:
        return 1
    
    # 중복 확인
    if user_settings.data_exists('user_name', user_name):
        return 1
    
    if user_settings.id_exists(user_name):
        return 1
    
    return 0

async def level_check(ip = ''):
    ip = ip_check() if ip == '' else ip

    other_set = {}
    other_set['ip'] = ip

    data = await python_to_golang('api_func_level', other_set)

    return data["data"]

async def acl_check(name = '', tool = '', topic_num = '', ip = '', memo = ''):
    ip = ip_check() if ip == '' else ip

    other_set = {}
    other_set['ip'] = ip
    other_set['name'] = name
    other_set['topic_number'] = topic_num
    other_set['tool'] = tool

    data = await python_to_golang('api_func_acl', other_set)

    result = 0 if data["data"] else 1

    if memo != '' and result == 0:
        other_set = {}
        other_set['ip'] = ip
        other_set['what'] = memo

        await python_to_golang('api_func_auth_post', other_set)

    return result

async def ban_check(ip = None, tool = ''):
    ip = ip_check() if not ip else ip
    tool = '' if not tool else tool

    other_set = {}
    other_set['ip'] = ip
    other_set['type'] = tool

    data = await python_to_golang('api_func_ban', other_set)
    data["ban"] = 1 if data["ban"] == "true" else 0

    return [data["ban"], data["ban_type"]]

async def ip_pas(raw_ip):
    other_set = {}
    
    return_data = 0
    if type(raw_ip) != type([]):
        get_ip = [raw_ip]
        return_data = 1
    else:
        get_ip = raw_ip

    for for_a in range(1, len(get_ip) + 1):
        other_set["data_" + str(for_a)] = get_ip[for_a - 1]

    data = await python_to_golang('api_func_ip_post', other_set)
    return data["data"][raw_ip] if return_data == 1 else data["data"]
        
# Func-edit
def get_edit_text_bottom(conn, tool = '') :
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

def get_edit_text_bottom_check_box(conn):
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

def do_edit_text_bottom_check_box_check(conn, data):
    db_data = get_other_setting_repository().get('copyright_checkbox_text')
    if db_data != '':
        if 'bottom_check_box_pass' in flask.session and flask.session['bottom_check_box_pass'] > 0:
            pass
        elif data != 'yes':
            return 1

    if not 'bottom_check_box_pass' in flask.session:
        flask.session['bottom_check_box_pass'] = 1
        
    return 0

async def do_edit_send_check(conn, data):
    db_data = get_other_setting_repository().get('edit_bottom_compulsion')
    if db_data != '':
        if await acl_check('', 'edit_bottom_compulsion') == 1:
            if data == '':
                return 1
    
    return 0

async def do_edit_slow_check(conn, do_type = 'edit'):
    settings = get_other_setting_repository()

    if do_type == 'edit':
        slow_edit = settings.get('slow_edit')
    else:
        # do_type == 'thread'
        slow_edit = settings.get('slow_thread')
    
    if slow_edit != '':
        if await acl_check('', 'slow_edit') == 1:
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

async def do_edit_filter(conn, data):
    ip = ip_check()
    if await acl_check(tool = 'edit_filter_pass') == 1:
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

                ban_insert(conn, 
                    ip,
                    r_time,
                    'edit filter',
                    '',
                    'tool:edit filter'
                )

                return 1

    return 0

def do_title_length_check(conn, name, check_type = 'document'):
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
def do_add_thread(conn, thread_code, thread_data, thread_top = '', thread_id = ''):
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
    
def do_reload_recent_thread(conn, topic_num, date, name = None, sub = None):
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

def add_user(conn, user_name, user_pw, user_email = '', user_encode = ''):
    user_settings = get_user_setting_repository()

    if user_encode == '':
        user_pw_hash = pw_encode(conn, user_pw)
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
    
def ua_plus(conn, u_id, u_ip, u_agent, time):
    rep_data = get_other_setting_repository().get('ua_get')
    if rep_data != '':
        pass
    else:
        get_user_agent_repository().add(u_id, u_ip, u_agent, time)

def ban_insert(conn, name, end, why, login, blocker, type_d = None, release = 0):
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

def history_plus_rc_max(conn, mode):
    history = get_history_repository()

    if history.count_recent_changes_by_type(mode) >= 200:
        rc_data = history.oldest_recent_change_ref_by_type(mode)
        if rc_data:
            history.delete_recent_change(rc_data[1], rc_data[0], mode)

def history_plus(conn, title, data, date, ip, send, leng, t_check = '', mode = ''):
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
        history_plus_rc_max(conn, 'normal')

        history.add_recent_change(title, id_data, date, 'normal')
    
    if mode != 'add' and mode != 'setting':
        history_plus_rc_max(conn, mode)

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
async def re_error(conn, data):
    if data == 0:
        if (await ban_check())[0] == 1:
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
        elif num == 34:
            update_repository = os.getenv("NAMU_UPDATE_REPOSITORY", "opennamu-forge/opennamu-forge")
            data = await get_lang("update_error") + ' <a href="https://github.com/' + html.escape(update_repository) + '">(Github)</a>'
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
