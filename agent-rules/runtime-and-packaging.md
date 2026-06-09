# Runtime and Packaging

## Runtime Stack

- Python 3.10+ only. Keep compatibility with Python 3.10; do not introduce 3.11-only or 3.12-only syntax.
- Flask 3.1+ async routes.
- Gunicorn is the production WSGI server.
- `uv` is the package manager and environment runner.
- Docker images currently use Python 3.11 and install dependencies with `uv sync --frozen`.

## Config Naming

- Project/runtime values from `.env`, CLI flags, DB connections, engine pools, Prometheus, Gunicorn, and process startup are `config`.
- Use names such as `DatabaseConfig`, `MonitoringConfig`, `*_config`, and `build_*_config_from_env()`.
- Do not use `settings` for project/runtime config; reserve `settings` for wiki/user/domain behavior.
- Runtime config builders return typed config objects. Convert to legacy dictionaries only at an explicit boundary such as `DatabaseConfig.to_db_set()`.

## uv Workflow

Use `pyproject.toml` as the source of truth for dependencies and `uv.lock` for resolved versions. Do not reintroduce `requirements.txt` or runtime dependency installers.

Install for development:

```bash
uv sync --extra performance --extra dev
```

Install runtime-only dependencies:

```bash
uv sync --frozen --no-dev --extra performance
```

Run commands through the project environment:

```bash
uv run python -m opennamu_forge.cli migrate
uv run python -m opennamu_forge.cli dev
uv run python -m opennamu_forge.cli serve --host 0.0.0.0 --port 3000 --workers 1 --threads 1
```

Do not add OS-specific shell or batch wrappers for normal project workflows. Prefer the Python CLI, uv, Docker Compose, and GitHub Actions.

Restart and shutdown process primitives belong in `opennamu_forge/presentation/runtime/process_control.py`. Route handlers may authorize and render the restart/shutdown screens, but must not call `subprocess.Popen`, `os._exit`, `sys.exit`, or start restart threads directly.

When dependencies change:

```bash
uv lock
```

## Runtime Updates

Do not add an in-app self-update route. Runtime code must not change git remotes, run `git reset --hard`, download release archives into the project tree, or overwrite source files from HTTP handlers. Ship updates through package, container, deployment, or operator-controlled CLI workflows.

## Theme Color

The Ringo skin reads `NAMU_THEME_COLOR` through `/forge/theme.css.cache_v1`. Accept only hex color values and fall back to `#00a495` for invalid input.

## Python 3.10+ Style

- Use Python 3.10+ typing where it improves clarity, such as `X | None` and `list[str]`.
- Use structural pattern matching only when it makes control flow simpler.
- Prefer small typed helpers around new infrastructure.
- Do not rewrite broad existing route code only to modernize syntax.

## Convention Tools

Use Ruff and ty through uv:

```bash
uv run --extra dev ruff check app.py opennamu_forge migrations tests opennamu_forge/presentation/shared/sql_dialect.py
uv run --extra dev ty check app.py opennamu_forge/config opennamu_forge/application opennamu_forge/infrastructure opennamu_forge/presentation/flask_factory.py opennamu_forge/presentation/theme.py opennamu_forge/presentation/__init__.py opennamu_forge/presentation/url_converters.py opennamu_forge/presentation/dependencies.py opennamu_forge/presentation/response_helpers.py opennamu_forge/presentation/encoding_helpers.py opennamu_forge/presentation/captcha_helpers.py opennamu_forge/presentation/email_helpers.py opennamu_forge/presentation/file_helpers.py opennamu_forge/presentation/authorization_helpers.py opennamu_forge/presentation/identity_helpers.py opennamu_forge/presentation/text_helpers.py opennamu_forge/presentation/user_validation_helpers.py opennamu_forge/presentation/route_registry.py opennamu_forge/presentation/runtime migrations tests
```

The route layer is migrated incrementally. Apply Ruff and ty to new 3-layer code, tests, and explicitly migrated route helper boundaries first, then expand the checked path as route modules move into `opennamu_forge/`.
