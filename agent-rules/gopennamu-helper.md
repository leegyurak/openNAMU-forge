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

When changing startup, routing, metrics, or DB config:

- Preserve the helper process lifecycle.
- Preserve the `NAMU_GOLANGPORT` contract.
- Keep `opennamu_forge/application/version.py` aligned with the expected GopenNAMU release.
- Avoid importing `app.py` from lightweight unit tests, because import starts DB bootstrap and the Go helper path.
- Treat removal of GopenNAMU as a separate migration project.
- Do not reintroduce a GopenNAMU client under `opennamu_forge/presentation/shared/`.
