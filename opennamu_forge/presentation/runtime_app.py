# Init
import atexit
import os
import signal
import sys
from pathlib import Path

if sys.version_info < (3, 10):
    raise RuntimeError('OpenNamu Forge requires Python 3.10 or newer.')

import flask
import requests

from opennamu_forge.config.env import load_env_file

load_env_file()

from opennamu_forge.application.startup import normalize_run_mode
from opennamu_forge.application.runtime_context import get_runtime_value
from opennamu_forge.application.version import VERSION_INFO
from opennamu_forge.config.database import build_database_config_from_env, is_sqlmodel_database_type
from opennamu_forge.config.runtime_database import apply_database_runtime_config
from opennamu_forge.infrastructure.logging import get_logger
from opennamu_forge.infrastructure.migrations import run_schema_migrations
from opennamu_forge.presentation.encoding_helpers import md5_replace, url_pas
from opennamu_forge.presentation.flask_factory import create_flask_app
from opennamu_forge.presentation.url_converters import register_url_converters

from opennamu_forge.presentation.text_helpers import (
    cut_100,
)
from opennamu_forge.presentation.response_helpers import load_lang
from opennamu_forge.presentation.dependencies import (
    get_other_setting_repository,
)
from opennamu_forge.presentation.runtime.gopennamu_process import (
    kill_port,
    start_gopennamu_process,
    terminate_gopennamu_process,
    wait_for_gopennamu_startup,
)
from opennamu_forge.presentation.runtime.scheduler import auto_do_something
from opennamu_forge.presentation.runtime.server_settings import resolve_server_settings
from opennamu_forge.presentation.runtime.startup_tasks import (
    ensure_startup_defaults,
    initialize_seed_data,
    select_go_helper_executable,
)
from opennamu_forge.presentation.route_registry import register_routes

from werkzeug.middleware.proxy_fix import ProxyFix

logger = get_logger(__name__)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
BIN_DIR = str(PROJECT_ROOT / "bin")
DATA_DIR = str(PROJECT_ROOT / "data")

os.makedirs(BIN_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

args = sys.argv
run_mode = ''
if len(args) > 1:
    run_mode = normalize_run_mode(args[1])

# Init-Version
version_list = VERSION_INFO

# Init-DB
data_db_set = build_database_config_from_env().to_db_set()
apply_database_runtime_config(data_db_set)

if is_sqlmodel_database_type(data_db_set):
    run_schema_migrations(data_db_set)

setup_tool = ''
old_ver = ""
try:
    old_ver = get_other_setting_repository().get('ver')
except:
    setup_tool = 'init'

if setup_tool != 'init':
    if old_ver != '':
        if int(version_list['c_ver']) > int(old_ver):
            setup_tool = 'update'
        else:
            setup_tool = 'normal'
    else:
        setup_tool = 'init'

logger.info("Run Mode : %s", run_mode)
logger.info("Setup Tool : %s", setup_tool)
logger.info("Old Version : %s", old_ver)

if run_mode != 'dev':
    file_name = select_go_helper_executable()
    local_file_path = os.path.join(BIN_DIR, file_name)

    if not (setup_tool == "normal" and os.path.exists(local_file_path)):
        if os.path.exists(local_file_path):
            logger.info('Remove Old Binary')
            os.remove(local_file_path)

        download_url = version_list["bin_link"] + file_name

        logger.info('Download New Binary File')
        response = requests.get(download_url, stream = True)
        if response.status_code == 200:
            with open(local_file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size = 8192):
                    file.write(chunk)

            logger.info('Complete Download')

if setup_tool == 'init':
    initialize_seed_data()

ensure_startup_defaults(version_list['c_ver'], run_mode)

app = create_flask_app(
    base_dir = str(PROJECT_ROOT),
    run_mode = run_mode,
    version = version_list['r_ver'],
    db_type = data_db_set['type'],
)

register_url_converters(app)

settings = get_other_setting_repository()
app.secret_key = settings.get('key')

# Init-DB_Data
server_set = resolve_server_settings(settings)

###
port_kill = kill_port(server_set["golang_port"])
logger.info("Golang port killed : %s", port_kill)

exe_name = select_go_helper_executable()
golang_process = start_gopennamu_process(
    bin_dir=BIN_DIR,
    executable_name=exe_name,
    golang_port=server_set["golang_port"],
    run_mode=run_mode,
)
wait_for_gopennamu_startup(data_db_set, server_set["golang_port"])

###

auto_do_something(data_db_set)

logger.info('Now running... http://127.0.0.1:%s', server_set['port'])

@app.before_request
def before_request_func():
    db_data = get_runtime_value('wiki_access_password')
    if db_data and db_data != '':
        access_password = db_data
        input_password = flask.request.cookies.get('opennamu_forge_wiki_access', ' ')
        if url_pas(access_password) != input_password:
            return '''
                <script>
                    "use strict";
                    function opennamu_forge_do_wiki_access() {
                        let password = document.getElementById('wiki_access').value;
                        document.cookie = 'opennamu_forge_wiki_access=' + encodeURIComponent(password) + '; path=/;';
                        history.go(0);
                    }
                </script>
                <h2>''' + load_lang('error_password_require_for_wiki_access') + '''</h2>
                <input class="__ON_INPUT__" type="password" id="wiki_access">
                <input class="__ON_INPUT__" type="submit" onclick="opennamu_forge_do_wiki_access();">
            '''

# Init-custom
if os.path.exists('custom.py'):
    from custom import custom_run
    custom_run('error', app)

register_routes(app, version_list=version_list, golang_process=golang_process)
def signal_handler(signal, frame):
    logger.info("EXIT SIGNAL RECEIVED")
    
    terminate_gopennamu_process(golang_process)
    os._exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

atexit.register(terminate_gopennamu_process, golang_process)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for = 1, x_proto = 1)

def run_app():
    if run_mode in ['dev']:
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

        app.jinja_options["cache_size"] = 0
        app.jinja_options["auto_reload"] = True
        app.jinja_options["bytecode_cache"] = None

        app.jinja_env.filters['md5_replace'] = md5_replace
        app.jinja_env.filters['load_lang'] = load_lang
        app.jinja_env.filters['cut_100'] = cut_100

        app.run(
            host = server_set['host'],
            port = int(server_set['port']),
            use_reloader = False,
            threaded = False,
            debug = True,
        )
    else:
        app.jinja_env.filters['md5_replace'] = md5_replace
        app.jinja_env.filters['load_lang'] = load_lang
        app.jinja_env.filters['cut_100'] = cut_100

        logger.info('Production WSGI server: gunicorn app:create_app()')
        app.run(
            host = server_set['host'],
            port = int(server_set['port']),
            use_reloader = False,
            threaded = False,
            debug = False,
        )
