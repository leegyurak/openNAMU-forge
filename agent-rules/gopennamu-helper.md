# GopenNAMU Helper

The Go binary is not incidental. Runtime startup downloads or reuses the platform-specific GopenNAMU binary from `opennamu_forge/application/version.py`, starts it on `NAMU_GOLANGPORT`, waits for `/compatible_api/test`, and terminates it with the Python process.

The current Python code delegates these responsibilities to GopenNAMU:

- Whole route handling for many list, history, search, user, watchlist, BBS, and API paths via `golang_view()`.
- Template rendering through `python_to_golang("post", path="template")`.
- ACL, ban, level, language, skin, wiki setting, alarm, page-view, and several API helpers through `/compatible_api/*`.
- Some markup/rendering fallbacks when the selected markup is not handled by the Python NamuMark renderer.

The call boundary is split by layer:

- `opennamu_forge/application/ports/gopennamu.py`: application-facing protocol.
- `opennamu_forge/infrastructure/gopennamu_client.py`: aiohttp client adapter. It must not import Flask or presentation helpers.
- `opennamu_forge/presentation/gopennamu_gateway.py`: Flask request/header/form extraction and runtime port lookup.

## Current Delegation Matrix

Python-owned behavior:

- Runtime process lifecycle: binary selection, startup, readiness wait, termination, signal/atexit registration.
- Flask route registration, URL converters, Prometheus route exposure, dynamic theme CSS, and app-level request hooks.
- Repository-backed writes that have been migrated to application services, including user registration, history mutation, discussion comment/recent-thread mutation, challenge progress refresh, and main settings form persistence.
- SQLModel repository access, migration execution, and runtime database config selection.

GopenNAMU-delegated behavior:

- Compatibility API calls whose behavior is still helper-owned: ACL evaluation, level lookup, ban checks, language lookup, skin name lookup, wiki custom/settings lookup, alarm posting, page view counters, and helper-backed JSON endpoints.
- Template rendering through `python_to_golang("post", path="template")` until the template bridge is replaced by a Python presenter/template path.
- Whole-route compatibility delegation through `golang_view()` and `python_to_golang("same")` for routes not yet represented as Python route modules.
- Rendering fallbacks that are not yet handled by the Python NamuMark renderer.

Migration rule:

- New Python-owned behavior must enter through an application service or a presentation helper with tests before removing a GopenNAMU call.
- Removing a helper-owned endpoint requires a compatibility test that preserves the HTTP/status/body contract currently returned through GopenNAMU.

When changing startup, routing, metrics, or DB config:

- Preserve the helper process lifecycle.
- Preserve the `NAMU_GOLANGPORT` contract.
- Keep `opennamu_forge/application/version.py` aligned with the expected GopenNAMU release.
- Avoid importing `app.py` from lightweight unit tests, because import starts DB bootstrap and the Go helper path.
- Treat removal of GopenNAMU as a separate migration project.
- Do not reintroduce a GopenNAMU client under `opennamu_forge/presentation/shared/`.
