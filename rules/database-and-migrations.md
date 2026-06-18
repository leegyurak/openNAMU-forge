# 데이터베이스와 마이그레이션

## 지원 DB

`NAMU_DB_TYPE` 값:

- `sqlite`
- `mysql`
- `postgresql` 또는 `postgres`

Network DB config:

- `NAMU_DB`
- `NAMU_DB_HOST`
- `NAMU_DB_PORT`
- `NAMU_DB_USER`
- `NAMU_DB_PASSWORD`

`app.py`는 startup 때 `.env`를 먼저 읽습니다. DB 선택은 `.env`/environment와 `DatabaseConfig`를 통해서만 처리합니다.

## SQLModel 기준

- SQLModel이 ORM 기준입니다.
- schema foundation은 `opennamu_forge/infrastructure/db_model.py`입니다.
- DB engine/session adapter는 `opennamu_forge/infrastructure/database_engine.py`에 둡니다.
- Alembic 실행 entrypoint는 `opennamu_forge/infrastructure/migrations.py`입니다.
- runtime DB 선택 상태는 `opennamu_forge/config/runtime_database.py`가 관리합니다.

## Route 금지 사항

- route module에서 raw SQL을 작성하지 않기.
- route module에서 DB connection/session class를 소유하지 않기.
- route module에서 SQL dialect 변환을 persistence behavior로 직접 사용하지 않기.
- presentation에 직접 sqlite/mysql/psycopg connection class를 만들지 않기.

## Migration 규칙

- runtime migration entrypoint는 `run_schema_migrations()`이며 Alembic `upgrade head`를 수행해야 합니다.
- 새 schema 작업은 SQLModel model 변경, Alembic revision, migration test 순서로 진행합니다.
- 파괴적 migration은 backup/rollback 계획 없이 추가하지 않습니다.
- PostgreSQL/MySQL/SQLite 차이는 SQL translation test와 integration test로 분리해 검증합니다.
- `.env.example`은 DB 관련 환경 변수가 추가되면 같이 갱신합니다.

## 테스트

- repository contract test와 mapper test를 route behavior 변경보다 먼저 추가합니다.
- DB dialect 작업은 SQL translation test와 SQLModel config test를 우선 작성합니다.
- 실제 MySQL/PostgreSQL integration test는 opt-in 환경변수나 Docker service 조건을 명확히 둡니다.
