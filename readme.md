[(en-US)](./readme-en.md) | [(ko-KR)](./readme.md)

# OpenNamu Forge

[![Python 3.10 이상](https://img.shields.io/badge/python->=%203.10-blue.svg)](https://python.org)
[![라이선스](https://img.shields.io/badge/license-BSD%203--Clause-lightgrey.svg)](./LICENSE)

OpenNamu Forge는 openNAMU를 기반으로 아키텍처, 런타임, 테스트, 관측 가능성, agent-friendly 기여 규칙을 현대화한 Python/Flask 위키 엔진입니다.

## 주요 기능

- openNAMU의 기존 위키 엔진 동작과 나무마크/마크다운 지원을 유지합니다.
- PostgreSQL, MySQL, SQLite를 선택할 수 있습니다.
- SQLModel 기반 ORM 레이어를 새 DB 작업의 기준으로 사용합니다.
- Gunicorn 기반 WSGI 실행을 기본 운영 방식으로 둡니다.
- Prometheus `/metrics`를 제공하며 `.env`로 path와 활성화 여부를 조정할 수 있습니다.
- agent가 일관되게 기여할 수 있도록 `AGENTS.md`와 `agent-rules/`에 작업 규칙을 분리했습니다.
- 신규/리팩터링 코드는 3-layer architecture를 따릅니다.

## 기술 스택

- Python 3.10+
- Flask 3.1+
- SQLModel / SQLAlchemy
- PostgreSQL, MySQL, SQLite
- Gunicorn
- Prometheus Flask Exporter
- uv
- pytest, coverage
- Ruff, ty

## 빠른 시작

```bash
cp .env.example .env
uv sync --extra performance --extra dev
uv run python -m opennamu_forge.cli migrate
uv run python -m opennamu_forge.cli dev
```

운영 방식에 가까운 로컬 실행:

```bash
uv run python -m opennamu_forge.cli serve --host 0.0.0.0 --port 3000 --workers 1 --threads 1
```

Docker Compose 실행:

```bash
cp .env.example .env
docker compose up --build
```

## 환경 변수

`.env`로 DB와 Prometheus 설정을 커스텀할 수 있습니다.

```env
NAMU_DB_TYPE=postgresql
NAMU_DB=data
NAMU_DB_HOST=opennamu-forge-db
NAMU_DB_PORT=5432
NAMU_DB_USER=opennamu_forge
NAMU_DB_PASSWORD=opennamu_forge_password

NAMU_THEME_COLOR=#00a495

NAMU_PROMETHEUS_ENABLED=true
NAMU_PROMETHEUS_PATH=/metrics
NAMU_PROMETHEUS_GROUP_BY=endpoint
```

지원 DB 타입:

- `sqlite`
- `mysql`
- `postgresql`

## 테스트와 품질 기준

```bash
uv run --extra dev pytest
uv run --extra dev python -m coverage run -m pytest
uv run --extra dev python -m coverage report --fail-under=90
uv run --extra dev ruff check app.py opennamu_forge migrations tests opennamu_forge/presentation/shared/sql_dialect.py
uv run --extra dev ty check app.py opennamu_forge/config opennamu_forge/application opennamu_forge/infrastructure opennamu_forge/presentation/flask_factory.py opennamu_forge/presentation/theme.py opennamu_forge/presentation/__init__.py opennamu_forge/presentation/url_converters.py opennamu_forge/presentation/dependencies.py opennamu_forge/presentation/response_helpers.py opennamu_forge/presentation/encoding_helpers.py opennamu_forge/presentation/captcha_helpers.py opennamu_forge/presentation/email_helpers.py opennamu_forge/presentation/file_helpers.py opennamu_forge/presentation/authorization_helpers.py opennamu_forge/presentation/identity_helpers.py opennamu_forge/presentation/text_helpers.py opennamu_forge/presentation/user_validation_helpers.py opennamu_forge/presentation/route_registry.py opennamu_forge/presentation/runtime migrations tests
```

테스트는 pytest 기반으로 작성합니다. 테스트 함수명은 `test_` prefix를 유지하면서 한국어로 작성합니다.
반복 케이스는 `pytest.mark.parametrize`로 작성하며 테스트 파일의 `for`/`while` 반복문은 금지합니다.

## 아키텍처

신규 코드는 `opennamu_forge/` 아래의 3-layer 구조를 따릅니다.

- `opennamu_forge/presentation/`: Flask app factory와 HTTP adapter
- `opennamu_forge/config/`: `.env` 기반 프로젝트/runtime config builder
- `opennamu_forge/application/`: use-case orchestration과 application service
- `opennamu_forge/infrastructure/`: DB, logging, monitoring, external process adapter

`settings`는 위키/유저/권한/스킨/문구 같은 도메인 동작 설정을 의미합니다.
`config`는 DB 연결, SQLModel engine/pool, Prometheus, Gunicorn, `.env` 기반 런타임 값을 의미합니다.
런타임 값에는 `*Config`, `*_config`, `build_*_config_from_env()` 명칭을 사용하고, 도메인 설정에는 `SettingKey`, `WikiSettingsService`, `*SettingRepository` 명칭을 사용합니다.

route 모듈은 raw SQL을 직접 사용하지 않습니다. DB 접근은 application port와 infrastructure repository를 통해 처리하며, SQL dialect 변환만 `opennamu_forge/presentation/shared/sql_dialect.py`에 격리합니다.

## 문서

- [AGENTS.md](./AGENTS.md): agent 작업 규칙의 진입점
- [docs/docker.md](./docs/docker.md): Docker와 Docker Compose 실행 가이드
- [agent-rules/runtime-and-packaging.md](./agent-rules/runtime-and-packaging.md): uv, Python, Gunicorn, Ruff, ty 규칙
- [agent-rules/database-and-migrations.md](./agent-rules/database-and-migrations.md): DB와 SQLModel 규칙
- [agent-rules/testing-and-coverage.md](./agent-rules/testing-and-coverage.md): pytest와 coverage 규칙
- [agent-rules/observability.md](./agent-rules/observability.md): Prometheus 규칙

## Upstream

OpenNamu Forge는 upstream openNAMU를 기반으로 합니다.

- [openNAMU](https://github.com/openNAMU/openNAMU)
- [GopenNAMU](https://github.com/openNAMU/GopenNAMU)

## 라이선스

OpenNamu Forge는 upstream openNAMU의 [BSD 3-Clause License](./LICENSE)를 따릅니다.
