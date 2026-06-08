from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass

from flask import Flask
from prometheus_client import CollectorRegistry
from prometheus_flask_exporter import PrometheusMetrics

from opennamu_forge.infrastructure.env import env_bool


@dataclass(frozen=True)
class MonitoringSettings:
    enabled: bool = True
    path: str = "/metrics"
    group_by: str = "endpoint"


def get_monitoring_settings(environ: Mapping[str, str] | None = None) -> MonitoringSettings:
    environ = os.environ if environ is None else environ
    path = environ.get("NAMU_PROMETHEUS_PATH", "/metrics").strip() or "/metrics"
    if not path.startswith("/"):
        path = "/" + path

    return MonitoringSettings(
        enabled=env_bool(environ, "NAMU_PROMETHEUS_ENABLED", default=True),
        path=path,
        group_by=environ.get("NAMU_PROMETHEUS_GROUP_BY", "endpoint").strip() or "endpoint",
    )


def configure_metrics(
    app: Flask,
    *,
    version: str,
    db_type: str,
    settings: MonitoringSettings | None = None,
) -> PrometheusMetrics | None:
    settings = get_monitoring_settings() if settings is None else settings
    if not settings.enabled:
        return None

    metrics = PrometheusMetrics(
        app,
        path=settings.path,
        group_by=settings.group_by,
        registry=CollectorRegistry(auto_describe=True),
    )
    metrics.info(
        "opennamu_forge_app_info",
        "OpenNamu Forge application build and runtime information",
        version=version,
        db_type=db_type,
    )
    return metrics
