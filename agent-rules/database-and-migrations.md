# Database and Migrations

## Supported Databases

Supported `NAMU_DB_TYPE` values:

- `sqlite`
- `mysql`
- `postgresql` or `postgres`

Network database config:

- `NAMU_DB`
- `NAMU_DB_HOST`
- `NAMU_DB_PORT`
- `NAMU_DB_USER`
- `NAMU_DB_PASSWORD`

`app.py` loads `.env` at startup before DB config is read. Keep `.env` local-only and update `.env.example` when adding DB environment keys.
Database selection must come from `.env`/environment through `DatabaseConfig`. Do not reintroduce legacy `data/set.json`, `data/mysql.json`, `data/postgresql.json`, or interactive DB prompts.

## SQLModel and Raw SQL

SQLModel is the ORM foundation. Route modules must not issue raw SQL directly; persistence access should go through application ports and infrastructure repositories. SQL dialect translation remains isolated in the shared SQL dialect module while routes move to repositories.

PostgreSQL support depends on:

- `opennamu_forge/config/database.py` for DB config from environment and SQLModel URL/pool config.
- `opennamu_forge/infrastructure/db_model.py` for SQLModel metadata.
- `opennamu_forge/infrastructure/database_engine.py` for SQLModel engine and session adapters.
- `opennamu_forge/infrastructure/migrations.py` for the Alembic migration entrypoint.
- `migrations/` for Alembic environment and versioned schema revisions.
- `opennamu_forge/presentation/shared/sql_dialect.py` for SQL dialect conversion.
- `opennamu_forge/config/runtime_database.py` for the runtime DB selection state consumed by repository factories.

Do not reintroduce `opennamu_forge/presentation/shared/db_connection.py` or direct sqlite/mysql/psycopg connection classes in presentation code.

## Migration Guidance

- `run_schema_migrations()` is the explicit runtime migration entrypoint and must run Alembic `upgrade head`.
- Treat `opennamu_forge/infrastructure/db_model.py` as the SQLModel schema foundation.
- New DB schema work must add SQLModel models first, then an Alembic revision under `migrations/versions/`, then migration tests.
- For PostgreSQL, verify SQL dialect conversion through `db_change()` and avoid DB-specific SQL in route files.
- Do not add destructive migrations without a backup and rollback plan.
- Add tests for SQL translation and SQLModel config before touching route behavior.
- Engine and connection pool behavior must be set through config/environment, not hardcoded inside models or repositories.
- Follow the FastAPI/SQLModel-style lifecycle: share the engine, scope sessions to a request/use-case boundary, and keep repository methods session-local and side-effect explicit.
