# Docker

OpenNamu Forge 런타임은 Python 3.10 이상을 지원합니다. Docker 이미지는 Python 3.11을 사용하며, 의존성은 `pyproject.toml`과 `uv.lock`을 기준으로 `uv`가 설치합니다.

## 이미지 빌드

```
docker build -t opennamu-forge:latest .
```

## 로컬 실행

```
cp .env.example .env
uv sync --extra performance --extra dev
uv run python -m opennamu_forge.cli migrate
uv run python -m opennamu_forge.cli dev
```

`.env`에서 `NAMU_DB_TYPE`(`sqlite`, `mysql`, `postgresql`)과 Prometheus 설정을 조정합니다. 기본 UI 색상은 `NAMU_THEME_COLOR=#00a495` 형식으로 바꿀 수 있습니다.

## 컨테이너 실행

```
docker run -p 3000:3000 -v data:/app/data --name opennamu-forge opennamu-forge:latest
docker run -p <host-port>:3000 -v <host-data_directory>:/app/data --name <docker-containername> opennamu-forge:latest
```

## PostgreSQL

`docker-compose.yaml`은 기본 DB로 PostgreSQL을 사용합니다.

```
docker compose up --build
```

웹 컨테이너는 다음 DB 설정을 읽습니다.

```
NAMU_DB_TYPE=postgresql
NAMU_DB=data
NAMU_DB_HOST=opennamu-forge-db
NAMU_DB_PORT=5432
NAMU_DB_USER=opennamu_forge
NAMU_DB_PASSWORD=opennamu_forge_password
```

컨테이너는 Python CLI를 통해 Gunicorn 기반 Flask WSGI 앱을 시작합니다.

```
python -m opennamu_forge.cli serve
```

Prometheus metric은 기본적으로 다음 경로에 노출됩니다.

```
http://localhost:3000/metrics
```

metric을 비활성화하려면 `NAMU_PROMETHEUS_ENABLED=false`를 사용합니다. 노출 경로를 바꾸려면 `NAMU_PROMETHEUS_PATH=/internal/metrics`처럼 지정합니다.
