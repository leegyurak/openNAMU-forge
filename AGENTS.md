# AGENTS.md

OpenNamu Forge는 openNAMU 동작을 유지하면서 Flask 런타임, SQLModel 기반 저장소, GopenNAMU 연동, Ringo 스킨, 테스트/관측 가능성 구조를 정리한 Python 위키 엔진입니다.

이 파일은 에이전트 진입점입니다. 세부 규칙은 `rules/`, 작업 절차는 `skills/`, 에이전트 운영 방식은 `agents/`를 먼저 보면 됩니다.

## 먼저 읽을 문서

- [에이전트 작업 흐름](agents/workflow.md)
- [아키텍처 규칙](rules/architecture.md)
- [런타임과 패키징](rules/runtime-and-packaging.md)
- [저장소와 DTO](rules/repository-and-dto.md)
- [데이터베이스와 마이그레이션](rules/database-and-migrations.md)
- [프론트엔드와 Ringo 스킨](rules/frontend-responsive.md)
- [GopenNAMU 경계](rules/gopennamu-helper.md)
- [테스트와 커버리지](rules/testing-and-coverage.md)
- [관측 가능성](rules/observability.md)

## 작업별 스킬

- [아키텍처 변경](skills/architecture.md)
- [백엔드 변경](skills/backend-change.md)
- [프론트엔드 Ringo 스킨](skills/frontend-ringo.md)
- [런타임과 GopenNAMU](skills/runtime-gopennamu.md)
- [테스트와 품질](skills/testing-quality.md)

## 핵심 경로

- `app.py`: lazy WSGI factory와 CLI 진입점.
- `opennamu_forge/presentation/runtime_app.py`: 런타임 조립, DB 마이그레이션, Flask 구성, route registry 설치, WSGI app 노출.
- `opennamu_forge/presentation/route_registry.py`: Flask URL rule 등록의 단일 지점.
- `opennamu_forge/presentation/runtime/`: 서버 옵션, GopenNAMU 프로세스, restart/shutdown, scheduler, startup task.
- `opennamu_forge/presentation/routes/`: Python이 직접 소유하는 HTTP route 모듈.
- `opennamu_forge/presentation/rendering/`: 문서 렌더링 adapter.
- `opennamu_forge/presentation/dependencies.py`: repository와 application service provider.
- `opennamu_forge/presentation/*_helpers.py`: route/presentation 보조 함수.
- `opennamu_forge/presentation/shared/sql_dialect.py`: SQL dialect 변환과 남은 저수준 호환 helper.
- `opennamu_forge/application/`: DTO, port, runtime context, application service.
- `opennamu_forge/infrastructure/`: SQLModel repository, mapper, DB engine, migration, logging, monitoring, 외부 client.
- `opennamu_forge/config/`: `.env` 기반 runtime config builder.
- `migrations/`: Alembic 환경과 schema revision.
- `views/ringo/`: 기본 React/TypeScript 스킨 source와 build asset.
- `views/main_css/`: route와 Ringo가 같이 쓰는 공용 static asset.

## 용어

- `settings`: 위키/유저/권한/스킨/문구 등 도메인 동작 설정.
- `config`: DB 연결, SQLModel engine/pool, Prometheus, Gunicorn, `.env` 등 런타임 설정.
- 내부 Python package는 `opennamu_forge`, 배포/저장소 이름은 `opennamu-forge`.

## 기본 명령

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

운영 방식에 가까운 로컬 WSGI 실행:

```bash
uv run python -m opennamu_forge.cli serve --host 0.0.0.0 --port 3000 --workers 1 --threads 1
```

## 절대 규칙

- 사용자가 명시하지 않은 route 동작 변경은 하지 않기.
- route module은 `opennamu_forge/presentation/routes/` 아래에만 두기.
- URL mapping은 `opennamu_forge/presentation/route_registry.py`에만 두기.
- runtime process, scheduler, restart/shutdown, startup task는 `opennamu_forge/presentation/runtime/` 아래에 두기.
- repository/application-service provider는 `opennamu_forge.presentation.dependencies`에서 가져오기.
- ACL, captcha, response, encoding, email, file, identity, text, user validation은 역할별 helper에서 가져오기.
- rendering code는 `opennamu_forge/presentation/rendering/` 아래에 두기.
- repository caller는 application port와 DTO를 통해 통신하기.
- repository 구현은 SQLModel row를 외부로 반환하지 않기.
- repository 구현에는 명시적 `if`/`for`/`while`, comprehension, generator, 불필요한 `list()` 변환을 넣지 않기.
- route module에서 raw SQL이나 직접 외부 HTTP I/O를 하지 않기.
- DB connection/session 소유권은 infrastructure에 두기.
- GopenNAMU 프로세스 생명주기와 `NAMU_GOLANGPORT` 계약을 유지하기.
- 테스트는 pytest, 한국어 `test_` 함수명, `pytest.mark.parametrize` matrix를 사용하기.
- 테스트 파일에는 명시적 loop와 comprehension을 쓰지 않기.
- HTML/CSS/JS 변경은 desktop/tablet/mobile 반응형 동작을 보존하고 회귀 테스트를 갱신하기.
- `/metrics`를 유지하고 민감하거나 cardinality가 높은 metric label을 만들지 않기.
- 환경 변수 기반 동작을 추가하면 `.env.example`, README, 관련 docs/tests를 함께 갱신하기.
