import subprocess
from pathlib import Path


def test_route_패키지는_presentation_routes_안에_있다():
    assert not Path("route").exists()
    assert Path("opennamu_forge/presentation/routes/__init__.py").exists()


def test_route_아래에는_tool_패키지를_두지_않는다():
    assert not Path("opennamu_forge/presentation/routes/tool").exists()
    assert Path("opennamu_forge/presentation/shared/__init__.py").exists()


def test_presentation_shared에는_gopennamu_client와_runtime_state를_두지_않는다():
    assert not Path("opennamu_forge/presentation/shared/gopennamu_client.py").exists()
    assert not Path("opennamu_forge/presentation/shared/runtime_state.py").exists()
    assert Path("opennamu_forge/infrastructure/gopennamu_client.py").exists()
    assert Path("opennamu_forge/application/runtime_context.py").exists()


def test_runtime_프로세스와_scheduler는_runtime_package에_둔다():
    runtime_app_source = Path("opennamu_forge/presentation/runtime_app.py").read_text()
    restart_route_source = Path("opennamu_forge/presentation/routes/main_sys_restart.py").read_text()
    shutdown_route_source = Path("opennamu_forge/presentation/routes/main_sys_shutdown.py").read_text()

    assert Path("opennamu_forge/presentation/runtime/__init__.py").exists()
    assert Path("opennamu_forge/presentation/runtime/gopennamu_process.py").exists()
    assert Path("opennamu_forge/presentation/runtime/scheduler.py").exists()
    assert Path("opennamu_forge/presentation/runtime/server_settings.py").exists()
    assert Path("opennamu_forge/presentation/runtime/process_control.py").exists()
    assert "def kill_port(" not in runtime_app_source
    assert "def back_up(" not in runtime_app_source
    assert "def daily_loop(" not in runtime_app_source
    assert "subprocess.Popen" not in restart_route_source
    assert "threading.Thread" not in restart_route_source
    assert "os._exit" not in restart_route_source
    assert "sys.exit" not in shutdown_route_source


def test_runtime_app은_route_등록을_route_registry에_위임한다():
    runtime_app_source = Path("opennamu_forge/presentation/runtime_app.py").read_text()

    assert Path("opennamu_forge/presentation/route_registry.py").exists()
    assert "register_routes(app" in runtime_app_source
    assert "app.route(" not in runtime_app_source
    assert "@app.get(" not in runtime_app_source
    assert "from opennamu_forge.presentation.routes import" not in runtime_app_source


def test_runtime_config는_settings_명칭을_사용하지_않는다():
    database_config_source = Path("opennamu_forge/config/database.py").read_text()
    monitoring_config_source = Path("opennamu_forge/config/monitoring.py").read_text()

    assert Path("opennamu_forge/config/__init__.py").exists()
    assert Path("opennamu_forge/config/runtime_database.py").exists()
    assert Path("opennamu_forge/config/startup_options.py").exists()
    assert not Path("opennamu_forge/infrastructure/database.py").exists()
    assert not Path("opennamu_forge/infrastructure/database_config.py").exists()
    assert not Path("opennamu_forge/infrastructure/env.py").exists()
    assert not Path("opennamu_forge/presentation/shared/db_connection.py").exists()
    assert "build_database_settings_from_env" not in database_config_source
    assert "MonitoringSettings" not in monitoring_config_source


def test_project_code는_wildcard_import를_사용하지_않는다():
    result = subprocess.run(
        ["rg", "-n", "import \\*", "opennamu_forge"],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 1, result.stdout


def test_legacy_self_update_route는_제거되어_있다():
    route_registry_source = Path("opennamu_forge/presentation/route_registry.py").read_text()
    admin_tool_source = Path("opennamu_forge/presentation/routes/main_tool_admin.py").read_text()

    assert not Path("opennamu_forge/presentation/routes/main_sys_update.py").exists()
    assert 'app.route("/update"' not in route_registry_source
    assert "app.route('/update'" not in route_registry_source
    assert 'href="/update"' not in admin_tool_source


def test_route는_직접_external_http_io를_수행하지_않는다():
    result = subprocess.run(
        ["rg", "-n", "urllib\\.request|urlopen\\(|urlretrieve\\(", "opennamu_forge/presentation/routes"],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 1, result.stdout
