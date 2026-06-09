from __future__ import annotations

from pathlib import Path

import flask

from opennamu_forge.config.monitoring import MonitoringConfig
from opennamu_forge.infrastructure.monitoring import configure_metrics


def create_flask_app(
    *,
    base_dir: str,
    run_mode: str,
    version: str,
    db_type: str,
    monitoring_config: MonitoringConfig | None = None,
) -> flask.Flask:
    app = flask.Flask(__name__, template_folder=str(Path(base_dir) / "views"))
    configure_metrics(app, version=version, db_type=db_type, config=monitoring_config)

    app.config["JSON_AS_ASCII"] = False
    app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 4233600

    if run_mode == "dev":
        app.config["TEMPLATES_AUTO_RELOAD"] = True
        app.config["DEBUG"] = True
        app.config["ENV"] = "development"

    return app
