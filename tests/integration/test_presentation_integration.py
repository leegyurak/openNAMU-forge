from opennamu_forge.application.startup import normalize_run_mode
from opennamu_forge.config.monitoring import MonitoringConfig, get_monitoring_config
from opennamu_forge.presentation.flask_factory import create_flask_app


def test_flask_factory는_metrics_endpoint를_제공한다(tmp_path):
    app = create_flask_app(
        base_dir=str(tmp_path),
        run_mode="",
        version="test-version",
        db_type="sqlite",
    )

    response = app.test_client().get("/metrics")

    assert response.status_code == 200
    assert b"opennamu_forge_app_info" in response.data
    assert b"test-version" in response.data


def test_flask_factory는_metrics_path를_커스텀한다(tmp_path):
    app = create_flask_app(
        base_dir=str(tmp_path),
        run_mode="",
        version="test-version",
        db_type="sqlite",
        monitoring_config=MonitoringConfig(path="/internal/metrics"),
    )

    client = app.test_client()

    assert client.get("/metrics").status_code == 404
    assert client.get("/internal/metrics").status_code == 200


def test_flask_factory는_metrics를_비활성화한다(tmp_path):
    app = create_flask_app(
        base_dir=str(tmp_path),
        run_mode="",
        version="test-version",
        db_type="sqlite",
        monitoring_config=MonitoringConfig(enabled=False),
    )

    assert app.test_client().get("/metrics").status_code == 404


def test_monitoring_config는_env에서_생성된다():
    config = get_monitoring_config(
        {
            "NAMU_PROMETHEUS_ENABLED": "off",
            "NAMU_PROMETHEUS_PATH": "internal/metrics",
            "NAMU_PROMETHEUS_GROUP_BY": "path",
        }
    )

    assert config.enabled is False
    assert config.path == "/internal/metrics"
    assert config.group_by == "path"


def test_flask_factory는_dev_설정을_적용한다(tmp_path):
    app = create_flask_app(
        base_dir=str(tmp_path),
        run_mode="dev",
        version="test-version",
        db_type="sqlite",
    )

    assert app.config["DEBUG"] is True
    assert app.config["TEMPLATES_AUTO_RELOAD"] is True
    assert app.config["ENV"] == "development"


def test_run_mode는_dev만_허용한다():
    assert normalize_run_mode("dev") == "dev"
    assert normalize_run_mode("prod") == ""
    assert normalize_run_mode("") == ""
