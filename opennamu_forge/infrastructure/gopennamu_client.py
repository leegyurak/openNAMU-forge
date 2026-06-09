from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from typing import Any

import aiohttp

from opennamu_forge.application.dto.gopennamu import GopenNamuRequestContext


class GopenNamuApiError(RuntimeError):
    pass


class GopenNamuAiohttpClient:
    def __init__(
        self,
        base_url: str,
        *,
        timeout_seconds: float = 10.0,
        session_factory: Callable[[], Any] | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.session_factory = session_factory

    async def call(
        self,
        func_name: str,
        *,
        other_set: Mapping[str, Any] | None = None,
        path: str = "",
        request_context: GopenNamuRequestContext | None = None,
    ) -> Any:
        payload = {} if other_set is None else other_set
        context = request_context or GopenNamuRequestContext()

        async with self._open_session() as session:
            if func_name == "same":
                return await self._same(session, context)
            if path:
                return await self._api_path(session, func_name, path, payload, context)
            return await self._compatible_api(session, func_name, payload, context)

    def _open_session(self) -> Any:
        if self.session_factory is not None:
            return self.session_factory()
        return aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout_seconds))

    async def _same(self, session: Any, context: GopenNamuRequestContext) -> str:
        if context.method.upper() == "POST":
            async with session.post(self._url(context.path), data=context.form_data, headers=dict(context.headers)) as response:
                return await response.text()
        async with session.get(self._url(context.path), headers=dict(context.headers)) as response:
            return await response.text()

    async def _api_path(
        self,
        session: Any,
        func_name: str,
        path: str,
        payload: Mapping[str, Any],
        context: GopenNamuRequestContext,
    ) -> Any:
        url = self._url("/api/" + path)
        if func_name == "get":
            async with session.get(url, headers=dict(context.headers)) as response:
                return await response.text()
        if func_name == "post":
            async with session.post(url, data=self._json_payload(payload), headers=dict(context.headers)) as response:
                return await response.text()
        if func_name == "get_json":
            async with session.get(url, headers=dict(context.headers)) as response:
                return await response.json()

        async with session.post(url, data=self._json_payload(payload), headers=dict(context.headers)) as response:
            return await response.json()

    async def _compatible_api(
        self,
        session: Any,
        func_name: str,
        payload: Mapping[str, Any],
        context: GopenNamuRequestContext,
    ) -> Any:
        async with session.post(
            self._url("/compatible_api/" + func_name),
            data=self._json_payload(payload),
            headers=dict(context.headers),
        ) as response:
            data = await response.json()

        if data.get("response") == "error":
            raise GopenNamuApiError(f"API returned error: {data}")
        return data

    def _url(self, path: str) -> str:
        return self.base_url + path

    def _json_payload(self, payload: Mapping[str, Any]) -> str:
        return json.dumps(payload, ensure_ascii=False)
