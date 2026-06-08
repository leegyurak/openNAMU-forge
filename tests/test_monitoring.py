import flask

from opennamu_forge.infrastructure.monitoring import MonitoringSettings, configure_metrics, get_monitoring_settings


def test_monitoring_settings는_기본값을_사용한다():
    settings = get_monitoring_settings({})

    assert settings.enabled is True
    assert settings.path == "/metrics"
    assert settings.group_by == "endpoint"


def test_monitoring_settings는_path_slash를_보정한다():
    settings = get_monitoring_settings({"NAMU_PROMETHEUS_PATH": "internal/metrics"})

    assert settings.path == "/internal/metrics"


def test_monitoring_settings는_빈_path와_group_by를_기본값으로_되돌린다():
    settings = get_monitoring_settings(
        {
            "NAMU_PROMETHEUS_PATH": "   ",
            "NAMU_PROMETHEUS_GROUP_BY": "   ",
        }
    )

    assert settings.path == "/metrics"
    assert settings.group_by == "endpoint"


def test_monitoring_settings는_알수없는_boolean이면_기본값을_유지한다():
    settings = get_monitoring_settings({"NAMU_PROMETHEUS_ENABLED": "maybe"})

    assert settings.enabled is True


def test_configure_metrics는_비활성화되면_route를_등록하지_않는다():
    app = flask.Flask(__name__)

    metrics = configure_metrics(
        app,
        version="test-version",
        db_type="sqlite",
        settings=MonitoringSettings(enabled=False),
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
