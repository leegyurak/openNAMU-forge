import flask

from opennamu_forge.config.monitoring import MonitoringConfig, get_monitoring_config
from opennamu_forge.infrastructure.monitoring import configure_metrics


def test_monitoring_config는_기본값을_사용한다():
    config = get_monitoring_config({})

    assert config.enabled is True
    assert config.path == "/metrics"
    assert config.group_by == "endpoint"


def test_monitoring_config는_path_slash를_보정한다():
    config = get_monitoring_config({"NAMU_PROMETHEUS_PATH": "internal/metrics"})

    assert config.path == "/internal/metrics"


def test_monitoring_config는_빈_path와_group_by를_기본값으로_되돌린다():
    config = get_monitoring_config(
        {
            "NAMU_PROMETHEUS_PATH": "   ",
            "NAMU_PROMETHEUS_GROUP_BY": "   ",
        }
    )

    assert config.path == "/metrics"
    assert config.group_by == "endpoint"


def test_monitoring_config는_알수없는_boolean이면_기본값을_유지한다():
    config = get_monitoring_config({"NAMU_PROMETHEUS_ENABLED": "maybe"})

    assert config.enabled is True


def test_configure_metrics는_비활성화되면_route를_등록하지_않는다():
    app = flask.Flask(__name__)

    metrics = configure_metrics(
        app,
        version="test-version",
        db_type="sqlite",
        config=MonitoringConfig(enabled=False),
    )

    assert metrics is None
    assert app.test_client().get("/metrics").status_code == 404


def test_configure_metrics는_반복_앱_생성에서_registry_충돌을_내지_않는다():
    first = flask.Flask("first")
    second = flask.Flask("second")

    configure_metrics(first, version="test-version", db_type="sqlite")
    configure_metrics(second, version="test-version", db_type="sqlite")

    assert first.test_client().get("/metrics").status_code == 200
    assert second.test_client().get("/metrics").status_code == 200
