# AGENTS.md

This repository is OpenNamu Forge, a modernized and agent-friendly Python/Flask wiki engine based on openNAMU. `app.py` is a lazy WSGI factory entrypoint; `opennamu_forge/presentation/runtime_app.py` wires runtime startup, database migration, Flask setup, route registry installation, and the WSGI app while delegating process and scheduler details to `opennamu_forge/presentation/runtime/`.

## Read First

- [Runtime and Packaging](agent-rules/runtime-and-packaging.md)
- [Architecture](agent-rules/architecture.md)
- [Repository and DTO Rules](agent-rules/repository-and-dto.md)
- [Frontend Responsive Design](agent-rules/frontend-responsive.md)
- [GopenNAMU Helper](agent-rules/gopennamu-helper.md)
- [Database and Migrations](agent-rules/database-and-migrations.md)
- [Testing and Coverage](agent-rules/testing-and-coverage.md)
- [Observability](agent-rules/observability.md)

## Core Paths

- `app.py`: side-effect-light WSGI factory and CLI entrypoint.
- `opennamu_forge/presentation/runtime_app.py`: runtime composition, DB migration trigger, Flask setup, route registry installation, and WSGI app exposure.
- `opennamu_forge/presentation/route_registry.py`: central Flask URL rule registration for route modules and GopenNAMU delegated views.
- `opennamu_forge/presentation/runtime/`: runtime-only orchestration helpers for server startup options, GopenNAMU process lifecycle, and scheduled background jobs.
- `opennamu_forge/presentation/routes/`: feature routes for wiki pages, edit flows, users, ACL, discussions, BBS, votes, settings, and APIs.
- `opennamu_forge/presentation/file_helpers.py`: image directory and default robots.txt helpers used by routes/runtime.
- `opennamu_forge/presentation/shared/func.py`: shared presentation helpers, ACL bridge, and remaining route adapter utilities.
- `opennamu_forge/presentation/rendering/`: document rendering adapters. Do not reintroduce shared `func_render*.py` modules.
- `opennamu_forge/presentation/dependencies.py`: explicit presentation dependency providers for repositories and application services.
- `opennamu_forge/presentation/response_helpers.py`: template bridge, language lookup, redirects, domain loading, and simple response rendering helpers.
- `opennamu_forge/presentation/encoding_helpers.py`: URL encoding, hashing, and JSON encode/decode helpers used by routes/runtime/rendering.
- `opennamu_forge/presentation/text_helpers.py`: small text, numeric, cache suffix, and random-key helpers used by routes/runtime.
- `opennamu_forge/presentation/shared/sql_dialect.py`: low-level helpers including SQL dialect conversion.
- `opennamu_forge/config/`: project/runtime config builders for `.env`, database, and monitoring values.
- `opennamu_forge/config/runtime_database.py`: runtime DB selection state used by repository factories.
- `opennamu_forge/config/startup_options.py`: startup option schema for host, ports, language, markup, and encryption choices.
- `opennamu_forge/infrastructure/db_model.py`: SQLModel metadata and existing table models.
- `opennamu_forge/infrastructure/database_engine.py`: SQLModel engine/session adapter using config-provided database values.
- `migrations/`: Alembic environment and versioned schema revisions.
- `opennamu_forge/presentation/`: Flask app factories and HTTP adapters.
- `opennamu_forge/application/`: use-case orchestration and application services.
- `opennamu_forge/application/version.py`: runtime, schema, skin, and GopenNAMU binary metadata.
- `opennamu_forge/infrastructure/`: DB, logging, monitoring, external process, and other adapters.
- The internal Python package is `opennamu_forge`; the distribution and repository name is `opennamu-forge`.
- `views/`: Jinja templates and static frontend assets. The default skin is `views/ringo`.

## Domain Terms

- `settings` means wiki/user/domain behavior settings, such as permissions, ACL-related options, skin choices, wiki text, and user preferences stored through repositories or `WikiSettingsService`.
- `config` means project/runtime config, such as DB connection values, SQLModel engine and pool options, Prometheus options, Gunicorn options, and values derived from `.env`.
- Do not name project/runtime config as `settings`. Use `*Config`, `*_config`, or `build_*_config_from_env()`.
- Do not name domain behavior settings as `config`. Use `SettingKey`, `WikiSettingsService`, or `*SettingRepository`.

## Default Commands

```bash
uv sync --extra performance --extra dev
uv run --extra dev pytest
uv run --extra dev pytest tests/integration
uv run --extra dev python -m coverage run -m pytest
uv run --extra dev python -m coverage report --fail-under=90
uv run --extra dev ruff check app.py opennamu_forge migrations tests opennamu_forge/presentation/shared/sql_dialect.py
uv run --extra dev ty check app.py opennamu_forge/config opennamu_forge/application opennamu_forge/infrastructure opennamu_forge/presentation/flask_factory.py opennamu_forge/presentation/theme.py opennamu_forge/presentation/__init__.py opennamu_forge/presentation/url_converters.py opennamu_forge/presentation/dependencies.py opennamu_forge/presentation/response_helpers.py opennamu_forge/presentation/encoding_helpers.py opennamu_forge/presentation/captcha_helpers.py opennamu_forge/presentation/email_helpers.py opennamu_forge/presentation/file_helpers.py opennamu_forge/presentation/authorization_helpers.py opennamu_forge/presentation/identity_helpers.py opennamu_forge/presentation/text_helpers.py opennamu_forge/presentation/user_validation_helpers.py opennamu_forge/presentation/route_registry.py opennamu_forge/presentation/runtime migrations tests
uv run python -m opennamu_forge.cli migrate
uv run python -m opennamu_forge.cli dev
```

Production-style local WSGI:

```bash
uv run python -m opennamu_forge.cli serve --host 0.0.0.0 --port 3000 --workers 1 --threads 1
```

## Non-Negotiables

- Preserve existing route behavior unless a task explicitly asks for a behavior change.
- Route modules belong inside `opennamu_forge/presentation/routes`; do not add new top-level `route/` modules.
- Do not add `opennamu_forge/presentation/routes/tool`; shared presentation helpers belong under `opennamu_forge/presentation/shared`.
- Repository callers must communicate through application-layer ports and DTOs, not SQLModel rows.
- Repository implementations must not contain explicit `if`/`for`/`while` control flow; express conditions and bulk behavior as SQL or delegate mapping outside the repository.
- Route modules must not use raw SQL. SQL dialect translation must stay outside routes and be covered by migration tests.
- Route modules and `runtime_app.py` must import repository/application-service providers from `opennamu_forge.presentation.dependencies`, not from `opennamu_forge.presentation.shared.func`.
- Route modules and runtime helpers must import ACL/ban/level helpers from `opennamu_forge.presentation.authorization_helpers`, not from `opennamu_forge.presentation.shared.func`.
- Route modules must import captcha helpers from `opennamu_forge.presentation.captcha_helpers`, not from `opennamu_forge.presentation.shared.func`.
- Route modules and `runtime_app.py` must import response helpers from `opennamu_forge.presentation.response_helpers`, not from `opennamu_forge.presentation.shared.func`.
- Route modules and `runtime_app.py` must import URL/hash/JSON helpers from `opennamu_forge.presentation.encoding_helpers`, not from `opennamu_forge.presentation.shared.func` or `shared.sql_dialect`.
- Route modules must import SMTP/email helpers from `opennamu_forge.presentation.email_helpers`, not from `opennamu_forge.presentation.shared.func`.
- Route modules and `runtime_app.py` must import file helpers from `opennamu_forge.presentation.file_helpers`, not from `opennamu_forge.presentation.shared.func`.
- Route modules must import identity/IP display helpers from `opennamu_forge.presentation.identity_helpers`, not from `opennamu_forge.presentation.shared.func`.
- Route modules and `runtime_app.py` must import text helpers from `opennamu_forge.presentation.text_helpers`, not from `opennamu_forge.presentation.shared.func`.
- Route modules must import user validation helpers from `opennamu_forge.presentation.user_validation_helpers`, not from `opennamu_forge.presentation.shared.func`.
- Route modules must not perform direct external HTTP I/O. Use application ports and infrastructure adapters such as `SkinInfoClient`.
- Rendering code belongs under `opennamu_forge/presentation/rendering`; do not recreate `opennamu_forge/presentation/shared/func_render.py` or `func_render_namumark.py`.
- Do not reintroduce `opennamu_forge/presentation/shared/db_connection.py`, `get_db_connect`, or presentation-owned DB connection classes.
- Do not remove existing DB bootstrap tables without a migration plan.
- Test case matrices must use `pytest.mark.parametrize`; explicit loops or comprehensions in test files are forbidden.
- Responsive behavior is non-negotiable for HTML/CSS/JS changes; update `agent-rules/frontend-responsive.md` tests and verify desktop/tablet/mobile behavior.
- Preserve the GopenNAMU process lifecycle and `NAMU_GOLANGPORT` contract unless removing that dependency is the task.
- Runtime process and scheduler code belongs under `opennamu_forge/presentation/runtime/`; do not add new process loops or background schedulers directly to `runtime_app.py`.
- Restart and shutdown process primitives belong under `opennamu_forge/presentation/runtime/process_control.py`; route handlers must not call `subprocess.Popen`, `os._exit`, `sys.exit`, or start restart threads directly.
- Runtime startup tasks belong under `opennamu_forge/presentation/runtime/startup_tasks.py`; do not add startup seed/default logic directly to `shared.func`.
- Route URL mapping belongs in `opennamu_forge/presentation/route_registry.py`; do not add direct `app.route(...)` blocks to `runtime_app.py`.
- Do not reintroduce the legacy in-app self-update route. HTTP handlers must not mutate git remotes, hard-reset the worktree, download release archives into the project tree, or overwrite source files.
- Keep `/metrics` available and avoid high-cardinality or sensitive metric labels.
- Keep `.env.example` in sync when adding environment-controlled runtime behavior.
