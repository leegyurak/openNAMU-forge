from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass

from opennamu_forge.config.env import env_bool


@dataclass(frozen=True)
class MonitoringConfig:
    enabled: bool = True
    path: str = "/metrics"
    group_by: str = "endpoint"


def get_monitoring_config(environ: Mapping[str, str] | None = None) -> MonitoringConfig:
    environ = os.environ if environ is None else environ
    path = environ.get("NAMU_PROMETHEUS_PATH", "/metrics").strip() or "/metrics"
    if not path.startswith("/"):
        path = "/" + path

    return MonitoringConfig(
        enabled=env_bool(environ, "NAMU_PROMETHEUS_ENABLED", default=True),
        path=path,
        group_by=environ.get("NAMU_PROMETHEUS_GROUP_BY", "endpoint").strip() or "endpoint",
    )
