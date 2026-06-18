# Refactoring TODO

이 문서는 현재 구조에서 남은 리팩터링 후보를 작업 가능한 TODO로 정리한다. TDD 전환 계획이 아니라, 현재 동작과 테스트 게이트를 유지하면서 냄새나는 구조를 걷어내기 위한 실행 목록이다.

## P0 - Shared Helper 해체

- [x] `opennamu_forge/presentation/shared/func.py` 의 route 의존성을 줄인다.
  - 현재 목표는 route가 `shared.func`에서 직접 import하는 helper를 0에 가깝게 줄이는 것이다.
  - 새 helper는 역할별로 `opennamu_forge/presentation/*_helpers.py` 또는 application service로 이동한다.
- [x] 비밀번호 관련 helper를 분리한다.
  - 대상: `pw_encode`, `pw_check`
  - 후보 위치: `opennamu_forge/presentation/password_helpers.py` 또는 application security service
  - route는 새 helper를 import하고 `shared.func` import를 제거한다.
- [x] edit validation helper를 분리한다.
  - 대상: `get_edit_text_bottom`, `get_edit_text_bottom_check_box`, `do_edit_text_bottom_check_box_check`, `do_edit_send_check`, `do_edit_slow_check`, `do_edit_filter`, `do_title_length_check`
  - 후보 위치: `opennamu_forge/presentation/edit_validation_helpers.py`
- [x] user mutation helper를 application service로 이동한다.
  - 대상: `add_user`
  - 목표: route가 user repository port와 DTO/service를 통해 사용자 생성을 요청하게 한다.
- [x] history mutation helper를 application service로 이동한다.
  - 대상: `history_plus_rc_max`, `history_plus`
  - 목표: history/recent-change 쓰기 정책을 route 밖으로 이동한다.
- [x] discussion/alarm helper를 application service로 이동한다.
  - 대상: `do_add_thread`, `do_reload_recent_thread`, `add_alarm`
- [x] error rendering helper를 response helper로 이동한다.
  - 대상: `re_error`
  - 목표: 오류 코드와 렌더링 책임을 `response_helpers` 또는 별도 error presenter에 둔다.
- [x] `shared.func` 축소 목표를 수치로 관리한다.
  - 현재 남은 파일 크기와 route import 수를 테스트 또는 문서에 기록한다.
  - 새 작업마다 route의 `from opennamu_forge.presentation.shared.func import ...` 항목을 줄인다.

## P0 - Route Thin Adapter 전환

- [x] route에서 비즈니스 분기와 저장소 호출을 application service로 이동한다.
  - 우선순위 후보: `view_w.py`, `recent_change.py`, `edit_upload.py`, `main_setting_main.py`, `user_challenge.py`
- [x] route 내부 HTML 문자열 조립을 template/presenter/helper로 이동한다.
  - 반복되는 `<form>`, list item, menu, pagination 문자열 조립부터 분리한다.
- [x] route가 직접 Flask session/request를 읽는 범위를 좁힌다.
  - route는 request DTO를 만들고 application service에 전달한다.
  - service는 Flask를 import하지 않는다.
- [x] route별 기대 동작을 integration test로 고정한다.
  - pytest 기반 유지
  - 테스트 함수명은 한국어 유지
  - 케이스 행렬은 `pytest.mark.parametrize`만 사용

## P1 - Config/Settings 용어와 경계 정리

- [x] runtime config 용어를 정리한다.
  - 후보: `db_set`, `to_db_set`
  - 목표 이름: `runtime_db_options`, `to_runtime_options` 등 현재 구조를 드러내는 이름
- [x] `settings`와 `config` 용어를 코드/문서/테스트에서 일관되게 적용한다.
  - `settings`: 위키/유저/권한/스킨/문구 같은 도메인 동작 설정
  - `config`: DB 연결, pool, Prometheus, Gunicorn, `.env` 기반 런타임 값
- [x] config 생성과 런타임 상태 저장을 분리한다.
  - config builder는 순수 값 객체 생성만 담당한다.
  - 런타임 선택 상태는 `runtime_database` 같은 명시적 boundary에 둔다.

## P1 - Repository/Mapper 규칙 강화

- [x] repository convention test를 더 엄격하게 만든다.
  - repository 내부 `if`, `for`, `while`, comprehension, `list()` 사용 금지 유지
  - 조건은 SQLAlchemy/SQLModel query expression으로 표현한다.
- [x] 동적 repository filter를 query spec/composer로 분리한다.
  - `or_(literal(not flag), condition)` 형태의 SQL tautology를 금지한다.
  - 예시 기준: sitemap title exclusion은 `WikiTitleSpec`이 SQLAlchemy expression을 조립한다.
- [x] repository 본문의 OR query 조합을 query spec/composer로 분리한다.
  - 예시 기준: `BbsPostCommentSpec`, `BacklinkRedirectSpec`, `UserAgentIdentitySpec`이 OR expression을 조립한다.
- [x] mapper batch 변환 규칙을 명확히 한다.
  - repository 내부 반복 금지를 유지하되, mapper에서 batch 변환을 허용할지 또는 tuple/map 기반으로 제한할지 결정한다.
  - 결정 후 `rules/repository-and-dto.md`와 convention test에 반영한다.
- [x] DTO 반환 경계를 재점검한다.
  - route/application이 SQLModel row를 직접 받지 않도록 guard test를 보강한다.
- [x] JPA-style repository method 이름과 where 조건의 대표 mismatch를 convention test로 막는다.
  - 우선 `*_by_title_type`, `*_by_ip_type`처럼 정적 equality 조건이 분명한 method부터 검사한다.

## P1 - Integration Test 현실화

- [x] MySQL/PostgreSQL integration test의 skip 조건을 점검한다.
  - CI에서 서비스 컨테이너로 실제 실행할 수 있으면 skip 대신 실행하도록 조정한다.
  - 로컬에서는 환경변수로 명시 opt-in 할 수 있게 유지한다.
- [x] SQLite/MySQL/PostgreSQL 모두 Alembic migration 후 기본 route 동작을 검증한다.
- [x] Prometheus `/metrics` 노출과 비활성화 설정을 integration test로 고정한다.

## P2 - Runtime 구조 정리

- [x] `runtime_app.py` 를 더 얇게 만든다.
  - Flask app composition, startup task 실행, signal wiring, serve entrypoint를 더 명확히 나눈다.
- [x] GopenNAMU helper 의존 범위를 계속 줄인다.
  - Python route가 직접 처리할 수 있는 기능과 helper binary 위임이 필요한 기능을 분리해서 기록한다.
  - 제거가 목표가 되는 경우 별도 migration plan을 작성한다.
- [x] process/scheduler 테스트 공백을 줄인다.
  - 낮은 coverage 모듈부터 분기 테스트를 보강한다.

## P2 - Frontend/Template 부채

- [x] `views/ringo`의 HTML/CSS/JS에 남은 이전 namespace와 문구를 재검색한다.
- [x] 반응형 요구사항을 route/template 변경마다 검증한다.
  - desktop/tablet/mobile viewport smoke test를 유지한다.
- [x] theme color 환경변수 적용 범위를 문서화한다.
  - `.env.example`, README, frontend responsive rule을 함께 갱신한다.

## Completion Gate

각 TODO를 닫을 때는 최소 아래 게이트를 통과해야 한다.

```bash
uv run --extra dev ruff check app.py opennamu_forge migrations tests opennamu_forge/presentation/shared/sql_dialect.py
uv run --extra dev ty check app.py opennamu_forge/config opennamu_forge/application opennamu_forge/infrastructure opennamu_forge/presentation/flask_factory.py opennamu_forge/presentation/theme.py opennamu_forge/presentation/__init__.py opennamu_forge/presentation/url_converters.py opennamu_forge/presentation/dependencies.py opennamu_forge/presentation/response_helpers.py opennamu_forge/presentation/encoding_helpers.py opennamu_forge/presentation/captcha_helpers.py opennamu_forge/presentation/email_helpers.py opennamu_forge/presentation/file_helpers.py opennamu_forge/presentation/authorization_helpers.py opennamu_forge/presentation/identity_helpers.py opennamu_forge/presentation/text_helpers.py opennamu_forge/presentation/user_validation_helpers.py opennamu_forge/presentation/route_registry.py opennamu_forge/presentation/runtime migrations tests
uv run --extra dev pytest
uv run --extra dev python -m coverage run -m pytest
uv run --extra dev python -m coverage report --fail-under=90
```
