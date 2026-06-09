from __future__ import annotations

from flask import Flask
from prometheus_client import CollectorRegistry
from prometheus_flask_exporter import PrometheusMetrics

from opennamu_forge.config.monitoring import MonitoringConfig, get_monitoring_config


def configure_metrics(
    app: Flask,
    *,
    version: str,
    db_type: str,
    config: MonitoringConfig | None = None,
) -> PrometheusMetrics | None:
    config = get_monitoring_config() if config is None else config
    if not config.enabled:
        return None

    metrics = PrometheusMetrics(
        app,
        path=config.path,
        group_by=config.group_by,
        registry=CollectorRegistry(auto_describe=True),
    )
    metrics.info(
        "opennamu_forge_app_info",
        "OpenNamu Forge application build and runtime information",
        version=version,
        db_type=db_type,
    )
    return metrics
