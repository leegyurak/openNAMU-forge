# Init
import importlib.util
import os
import sys
from pathlib import Path

from opennamu_forge.application.startup import normalize_run_mode
from opennamu_forge.application.version import VERSION_INFO
from opennamu_forge.config.database import build_database_config_from_env, is_sqlmodel_database_type
from opennamu_forge.config.env import load_env_file
from opennamu_forge.config.runtime_database import apply_database_runtime_config
from opennamu_forge.infrastructure.logging import get_logger
from opennamu_forge.infrastructure.migrations import run_schema_migrations
from opennamu_forge.presentation.dependencies import get_other_setting_repository
from opennamu_forge.presentation.flask_factory import create_flask_app
from opennamu_forge.presentation.route_registry import register_routes
from opennamu_forge.presentation.runtime.flask_hooks import (
    apply_proxy_fix,
    enable_dev_template_reload,
    register_template_filters,
    register_wiki_access_gate,
)
from opennamu_forge.presentation.runtime.gopennamu_binary import ensure_gopennamu_binary
from opennamu_forge.presentation.runtime.gopennamu_process import (
    kill_port,
    start_gopennamu_process,
    terminate_gopennamu_process,
    wait_for_gopennamu_startup,
)
from opennamu_forge.presentation.runtime.process_control import register_termination_handlers
from opennamu_forge.presentation.runtime.scheduler import auto_do_something
from opennamu_forge.presentation.runtime.server_settings import resolve_server_settings
from opennamu_forge.presentation.runtime.startup_tasks import (
    ensure_startup_defaults,
    initialize_seed_data,
    select_go_helper_executable,
)
from opennamu_forge.presentation.url_converters import register_url_converters

load_env_file()

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
database_runtime_options = build_database_config_from_env().to_runtime_options()
apply_database_runtime_config(database_runtime_options)

if is_sqlmodel_database_type(database_runtime_options):
    run_schema_migrations(database_runtime_options)

setup_tool = ''
old_ver = ""
try:
    old_ver = get_other_setting_repository().get('ver')
except Exception:
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

ensure_gopennamu_binary(
    run_mode=run_mode,
    setup_tool=setup_tool,
    bin_dir=BIN_DIR,
    version_list=version_list,
    executable_name=select_go_helper_executable(),
    logger=logger,
)

if setup_tool == 'init':
    initialize_seed_data()

ensure_startup_defaults(version_list['c_ver'], run_mode)

app = create_flask_app(
    base_dir = str(PROJECT_ROOT),
    run_mode = run_mode,
    version = version_list['r_ver'],
    db_type = database_runtime_options['type'],
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
    database_runtime_options=database_runtime_options,
)
wait_for_gopennamu_startup(database_runtime_options, server_set["golang_port"])

###

auto_do_something(database_runtime_options)

logger.info('Now running... http://127.0.0.1:%s', server_set['port'])

register_wiki_access_gate(app)

# Init-custom
if os.path.exists('custom.py'):
    custom_spec = importlib.util.spec_from_file_location("opennamu_forge_custom", "custom.py")
    if custom_spec is not None and custom_spec.loader is not None:
        custom_module = importlib.util.module_from_spec(custom_spec)
        custom_spec.loader.exec_module(custom_module)
        custom_run = getattr(custom_module, "custom_run")
        custom_run('error', app)

register_routes(app, version_list=version_list, golang_process=golang_process)
register_termination_handlers(golang_process, terminate_gopennamu_process)

apply_proxy_fix(app)

def run_app():
    if run_mode in ['dev']:
        enable_dev_template_reload(app)
        register_template_filters(app)

        app.run(
            host = server_set['host'],
            port = int(server_set['port']),
            use_reloader = False,
            threaded = False,
            debug = True,
        )
    else:
        register_template_filters(app)

        logger.info('Production WSGI server: gunicorn app:create_app()')
        app.run(
            host = server_set['host'],
            port = int(server_set['port']),
            use_reloader = False,
            threaded = False,
            debug = False,
        )
