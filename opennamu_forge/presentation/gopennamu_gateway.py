from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import flask

from opennamu_forge.application.dto.gopennamu import GopenNamuRequestContext
from opennamu_forge.application.runtime_context import get_runtime_value
from opennamu_forge.infrastructure.gopennamu_client import GopenNamuAiohttpClient
from opennamu_forge.presentation.shared.sql_dialect import ip_check


def build_gopennamu_request_context() -> GopenNamuRequestContext:
    if not flask.has_request_context():
        return GopenNamuRequestContext()

    headers: dict[str, str] = {"X-Forwarded-For": ip_check()}
    cookie = flask.request.headers.get("Cookie")
    if cookie is not None:
        headers["Cookie"] = cookie

    form_data = flask.request.form.to_dict(flat=False) if flask.request.method == "POST" else None
    return GopenNamuRequestContext(
        method=flask.request.method,
        path=flask.request.path,
        headers=headers,
        form_data=form_data,
    )

def build_gopennamu_client() -> GopenNamuAiohttpClient:
    port = get_runtime_value("setup_golang_port")
    if port is None:
        raise RuntimeError("GopenNAMU port is not configured.")
    return GopenNamuAiohttpClient(base_url="http://127.0.0.1:" + str(port))

async def python_to_golang(
    func_name: str,
    other_set: Mapping[str, Any] | None = None,
    path: str = "",
) -> Any:
    return await build_gopennamu_client().call(
        func_name,
        other_set=other_set,
        path=path,
        request_context=build_gopennamu_request_context(),
    )
