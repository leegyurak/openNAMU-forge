# GopenNAMU 경계

GopenNAMU는 현재 런타임의 필수 helper입니다. Python runtime은 플랫폼별 GopenNAMU binary를 준비하고, `NAMU_GOLANGPORT`에서 실행하며, `/compatible_api/test` readiness를 기다린 뒤 Python process 종료와 함께 정리합니다.

## 현재 위임 영역

- `golang_view()`와 `python_to_golang("same")`을 통한 일부 whole-route delegation.
- `python_to_golang("post", path="template")`을 통한 template rendering.
- ACL, ban, level, language, skin, wiki setting, alarm, page-view 등 `/compatible_api/*`.
- Python NamuMark renderer가 담당하지 않는 rendering fallback.

## 계층별 소유권

- `opennamu_forge/application/ports/gopennamu.py`: application-facing protocol.
- `opennamu_forge/infrastructure/gopennamu_client.py`: aiohttp client adapter. Flask를 import하지 않습니다.
- `opennamu_forge/presentation/gopennamu_gateway.py`: Flask request/header/form 추출과 runtime port 조회.
- `opennamu_forge/presentation/runtime/gopennamu_process.py`: helper process lifecycle.

## Python 소유 영역

- Flask app factory, route registry, URL converter, dynamic theme CSS.
- Prometheus route exposure와 app-level request hook.
- SQLModel repository와 migration 실행.
- application service로 이동된 user registration, history mutation, discussion mutation, challenge refresh, main settings form persistence.

## 변경 규칙

- 새 Python-owned behavior는 application service나 focused presentation helper로 들어가고 테스트를 먼저 둡니다.
- helper-owned endpoint를 제거하려면 기존 HTTP/status/body 계약을 보존하는 compatibility test가 필요합니다.
- `NAMU_GOLANGPORT` 계약을 유지합니다.
- `opennamu_forge/application/version.py`의 GopenNAMU release metadata를 맞춥니다.
- 가벼운 unit test에서 `app.py` import로 DB bootstrap/GopenNAMU path를 건드리지 않게 합니다.
- GopenNAMU 제거는 별도 migration project로 다룹니다.
