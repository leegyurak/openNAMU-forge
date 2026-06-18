# 아키텍처 규칙

OpenNamu Forge의 새 코드와 리팩터링 코드는 3-layer 구조를 따릅니다.

## 계층

- Presentation: Flask app factory, route module, request/response glue, presenter, rendering adapter, static asset bridge.
- Application: use case, DTO, port, runtime context, service-level policy, orchestration.
- Infrastructure: SQLModel model/repository, mapper, engine/session, migration, logging, monitoring, subprocess, network client.

`opennamu_forge/config/`는 도메인 계층이 아니라 runtime config 경계입니다. `.env`를 읽고 typed config object를 만들 수는 있지만, domain behavior, repository, Flask route, SQLModel session, process lifecycle은 넣지 않습니다.

## 현재 배치

- `opennamu_forge/presentation/`: presentation layer.
- `opennamu_forge/presentation/routes/`: Python route module.
- `opennamu_forge/presentation/route_registry.py`: Flask URL rule 등록 단일 지점.
- `opennamu_forge/presentation/runtime/`: startup, scheduler, process control, GopenNAMU lifecycle.
- `opennamu_forge/presentation/rendering/`: document rendering adapter.
- `opennamu_forge/presentation/dependencies.py`: repository/service provider.
- `opennamu_forge/presentation/*_helpers.py`: 역할별 presentation helper.
- `opennamu_forge/presentation/shared/sql_dialect.py`: SQL dialect 변환과 남은 저수준 helper.
- `opennamu_forge/application/dto/`: 계층 사이 DTO.
- `opennamu_forge/application/ports/`: infrastructure adapter protocol.
- `opennamu_forge/application/services/`: application service.
- `opennamu_forge/infrastructure/`: concrete adapter.
- `opennamu_forge/infrastructure/mappers/`: SQLModel row와 DTO 변환.
- `opennamu_forge/config/`: typed runtime config builder.
- `views/ringo/`: 기본 React/TypeScript skin.
- `views/main_css/`: route와 Ringo가 공유하는 static asset.

## 의존 방향

- Presentation은 Application에 의존할 수 있고, adapter wiring 지점에서만 Infrastructure concrete class를 알 수 있습니다.
- Application은 Flask, SQLModel session, concrete repository를 import하지 않습니다.
- Infrastructure는 Config와 외부 library에 의존할 수 있지만 Flask request/session state를 알면 안 됩니다.
- Network client는 Infrastructure에 두고, Presentation은 request context 조립까지만 담당합니다.

## Route와 Helper

- 새 route나 이동 route는 `opennamu_forge/presentation/routes/`에 둡니다.
- URL rule은 `opennamu_forge/presentation/route_registry.py`에만 추가합니다.
- `runtime_app.py`는 runtime 조립과 registry 설치만 담당합니다.
- route는 역할별 helper를 직접 import합니다:
  - `authorization_helpers`
  - `captcha_helpers`
  - `response_helpers`
  - `encoding_helpers`
  - `email_helpers`
  - `file_helpers`
  - `identity_helpers`
  - `text_helpers`
  - `user_validation_helpers`
- repository/service provider는 `opennamu_forge.presentation.dependencies`에서 가져옵니다.

## Persistence 경계

- route에서 raw SQL을 작성하지 않습니다.
- route가 persistence를 써야 하면 application port, DTO, service, dependency provider를 거칩니다.
- repository는 Infrastructure에 두고 DTO/scalar만 반환합니다.
- SQLModel row to DTO 변환은 mapper에서 처리합니다.
- `settings` 읽기/쓰기는 `WikiSettingsService`, `SettingKey`, repository/provider 경계를 우선 사용합니다.

## Refactor 절차

1. 현재 동작을 characterization test나 integration test로 고정합니다.
2. 새 behavior의 계층 소유자를 정합니다.
3. route signature, URL, status code, response shape를 유지합니다.
4. stale wrapper와 삭제된 import path는 같은 변경에서 정리합니다.
5. schema나 public URL 변경이 있으면 migration plan을 남깁니다.
