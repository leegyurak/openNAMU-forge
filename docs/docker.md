## Docker
```
docker build -t opennamu-forge:latest .
```

OpenNamu Forge runtime supports Python 3.10 or newer. The Docker images use Python 3.11.
Dependencies are resolved with `uv` from `pyproject.toml` and `uv.lock`.

## Local setup

```
cp .env.example .env
uv sync --extra performance --extra dev
uv run python -m opennamu_forge.cli migrate
uv run python -m opennamu_forge.cli dev
```

Edit `.env` to choose `NAMU_DB_TYPE` (`sqlite`, `mysql`, `postgresql`) and to customize Prometheus settings.
Use `NAMU_THEME_COLOR=#00a495` to customize the primary UI color.

## Start
```
docker run -p 3000:3000 -v data:/app/data --name opennamu-forge opennamu-forge:latest
docker run -p <host-port>:3000 -v <host-data_directory>:/app/data --name <docker-containername> opennamu-forge:latest
```

## PostgreSQL
`docker-compose.yaml` uses PostgreSQL by default.

```
docker compose up --build
```

The web container reads these database settings:

```
NAMU_DB_TYPE=postgresql
NAMU_DB=data
NAMU_DB_HOST=opennamu-forge-db
NAMU_DB_PORT=5432
NAMU_DB_USER=opennamu_forge
NAMU_DB_PASSWORD=opennamu_forge_password
```

The container starts the Flask WSGI app with Gunicorn through the Python CLI:

```
python -m opennamu_forge.cli serve
```

Prometheus metrics are exposed at:

```
http://localhost:3000/metrics
```

Use `NAMU_PROMETHEUS_ENABLED=false` to disable metrics or `NAMU_PROMETHEUS_PATH=/internal/metrics` to expose them on a custom path.

Use `NAMU_UPDATE_REPOSITORY=owner/repository` to customize the in-app update source.
