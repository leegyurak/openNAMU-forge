# Runtime and Packaging

## Runtime Stack

- Python 3.10+ only. Keep compatibility with Python 3.10; do not introduce 3.11-only or 3.12-only syntax.
- Flask 3.1+ async routes.
- Gunicorn is the production WSGI server.
- `uv` is the package manager and environment runner.
- Docker images currently use Python 3.11 and install dependencies with `uv sync --frozen`.

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

When dependencies change:

```bash
uv lock
```

## Update Source

The in-app update flow uses `NAMU_UPDATE_REPOSITORY`, defaulting to `opennamu-forge/opennamu-forge`. Do not hard-code upstream openNAMU update URLs in runtime code.

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
uv run --extra dev ruff check app.py opennamu_forge migrations tests opennamu_forge/presentation/routes/tool/func_tool.py
uv run --extra dev ty check app.py opennamu_forge/application opennamu_forge/infrastructure opennamu_forge/presentation/flask_factory.py opennamu_forge/presentation/theme.py opennamu_forge/presentation/__init__.py migrations tests
```

The route layer is migrated incrementally. Apply Ruff and ty to new 3-layer code, tests, and explicitly migrated route helper boundaries first, then expand the checked path as route modules move into `opennamu_forge/`.
