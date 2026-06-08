# Database and Migrations

## Supported Databases

Supported `NAMU_DB_TYPE` values:

- `sqlite`
- `mysql`
- `postgresql` or `postgres`

Network database settings:

- `NAMU_DB`
- `NAMU_DB_HOST`
- `NAMU_DB_PORT`
- `NAMU_DB_USER`
- `NAMU_DB_PASSWORD`

`app.py` loads `.env` at startup before DB configuration is read. Keep `.env` local-only and update `.env.example` when adding DB environment keys.

## SQLModel and Raw SQL

SQLModel is the ORM foundation. Existing routes still use the cursor API and SQLite-style `?` placeholders, so route SQL must continue going through `db_change()` until the feature is moved to application/infrastructure services.

PostgreSQL support depends on:

- `opennamu_forge/infrastructure/db_model.py` for SQLModel metadata.
- `opennamu_forge/infrastructure/database_config.py` for SQLModel engine, session, and pool configuration.
- `opennamu_forge/infrastructure/migrations.py` for the Alembic migration entrypoint.
- `migrations/` for Alembic environment and versioned schema revisions.
- `opennamu_forge/presentation/routes/tool/func_tool.py` for SQL dialect compatibility conversion.
- `opennamu_forge/presentation/routes/tool/func.py` for DB configuration and connection setup.

## Migration Guidance

- `run_schema_migrations()` is the explicit runtime migration entrypoint and must run Alembic `upgrade head`.
- Treat `opennamu_forge/infrastructure/db_model.py` as the SQLModel schema foundation and `get_db_table_list()` as the raw SQL bootstrap path for DB types that are not yet SQLModel-initialized.
- New DB schema work must add SQLModel models first, then an Alembic revision under `migrations/versions/`, then migration tests.
- For PostgreSQL, verify raw SQL through `db_change()` and avoid DB-specific SQL in route files.
- Do not add destructive migrations without a backup and rollback plan.
- Add tests for SQL translation and SQLModel configuration before touching route behavior.
- Engine and connection pool behavior must be configured through settings/environment, not hardcoded inside models or repositories.
- Follow the FastAPI/SQLModel-style lifecycle: share the engine, scope sessions to a request/use-case boundary, and keep repository methods session-local and side-effect explicit.
