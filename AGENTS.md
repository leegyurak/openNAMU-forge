# AGENTS.md

This repository is OpenNamu Forge, a modernized and agent-friendly Python/Flask wiki engine based on openNAMU. `app.py` is a lazy WSGI factory entrypoint; `opennamu_forge/presentation/runtime_app.py` performs runtime startup, initializes the database through Alembic, starts the local GopenNAMU helper binary from `bin/`, registers Flask routes, and exposes the WSGI app.

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
- `opennamu_forge/presentation/runtime_app.py`: process startup, DB migration, Flask setup, route registration, scheduler startup.
- `opennamu_forge/presentation/routes/`: feature routes for wiki pages, edit flows, users, ACL, discussions, BBS, votes, settings, and APIs.
- `opennamu_forge/presentation/routes/tool/func.py`: shared legacy helpers, DB connection setup, raw SQL bootstrap, ACL bridge, rendering helpers.
- `opennamu_forge/presentation/routes/tool/func_tool.py`: low-level helpers including SQL dialect conversion.
- `opennamu_forge/infrastructure/db_model.py`: SQLModel metadata, ORM session/engine helpers, and existing table models.
- `migrations/`: Alembic environment and versioned schema revisions.
- `opennamu_forge/presentation/`: Flask app factories and HTTP adapters.
- `opennamu_forge/application/`: use-case orchestration and application services.
- `opennamu_forge/application/version.py`: runtime, schema, skin, and GopenNAMU binary metadata.
- `opennamu_forge/infrastructure/`: DB, logging, monitoring, external process, and other adapters.
- The internal Python package is `opennamu_forge`; the distribution and repository name is `opennamu-forge`.
- `views/`: Jinja templates and static frontend assets. The default skin is `views/ringo`.

## Default Commands

```bash
uv sync --extra performance --extra dev
uv run --extra dev pytest
uv run --extra dev pytest tests/integration
uv run --extra dev python -m coverage run -m pytest
uv run --extra dev python -m coverage report --fail-under=90
uv run --extra dev ruff check app.py opennamu_forge migrations tests opennamu_forge/presentation/routes/tool/func_tool.py
uv run --extra dev ty check app.py opennamu_forge/application opennamu_forge/infrastructure opennamu_forge/presentation/flask_factory.py opennamu_forge/presentation/theme.py opennamu_forge/presentation/__init__.py migrations tests
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
- Repository callers must communicate through application-layer ports and DTOs, not SQLModel rows.
- Repository implementations must not contain explicit `if`/`for`/`while` control flow; express conditions and bulk behavior as SQL or delegate mapping outside the repository.
- Keep raw SQL behind `db_change()` until the surrounding feature is fully moved to SQLModel.
- Do not remove existing DB bootstrap tables without a migration plan.
- Test case matrices must use `pytest.mark.parametrize`; explicit loops or comprehensions in test files are forbidden.
- Responsive behavior is non-negotiable for HTML/CSS/JS changes; update `agent-rules/frontend-responsive.md` tests and verify desktop/tablet/mobile behavior.
- Preserve the GopenNAMU process lifecycle and `NAMU_GOLANGPORT` contract unless removing that dependency is the task.
- Keep `/metrics` available and avoid high-cardinality or sensitive metric labels.
- Keep `.env.example` in sync when adding environment-controlled runtime behavior.
