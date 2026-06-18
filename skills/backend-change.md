# 백엔드 변경 스킬

라우트, 헬퍼, 서비스, 저장소, DTO, 애플리케이션 동작을 변경할 때 사용하는 절차입니다. 기본 원칙은 현재 계층 구조를 유지하면서 동작 변경을 작게 고정하는 것입니다.

## 소유 계층 확인

- HTTP 입출력, 요청 파라미터, 응답 형식은 `opennamu_forge/presentation/routes/`가 담당합니다.
- 반복되는 Flask 접착 코드는 `opennamu_forge/presentation/*_helpers.py`로 분리합니다.
- 도메인 정책과 사용 사례 조합은 `opennamu_forge/application/services/`에 둡니다.
- DB 읽기/쓰기와 외부 시스템 어댑터는 `opennamu_forge/infrastructure/`에 둡니다.
- SQLModel row와 DTO 매핑은 `opennamu_forge/infrastructure/mappers/`에 둡니다.

## 구현 절차

1. 기존 라우트와 테스트를 먼저 읽고 URL, 상태 코드, 응답 본문, 리다이렉트 동작을 파악합니다.
2. 동작을 바꾸기 전에 가장 가까운 특성화 테스트를 추가합니다.
3. 라우트 시그니처, URL, 응답 모양은 요청된 변경이 아니면 유지합니다.
4. 계층 사이의 데이터는 애플리케이션 포트와 DTO로 전달합니다.
5. 라우트에는 raw SQL, SQL dialect 변환, DB 세션 생성 코드를 넣지 않습니다.
6. 저장소 구현에는 명시적인 `if`, `for`, `while` 제어 흐름을 늘리지 않고 SQL 조건 또는 매퍼로 표현합니다.
7. 대상 테스트를 먼저 돌리고, 공유 동작이면 전체 테스트와 타입 검사를 확장합니다.

## 선호 패턴

- 라우트에서 필요한 의존성은 `opennamu_forge.presentation.dependencies`의 provider를 사용합니다.
- ACL, ban, level 판단은 `authorization_helpers`를 통해 호출합니다.
- 응답, URL/hash/JSON, captcha, email, file, identity, text, user validation 관련 기능은 각각의 전용 helper에서 가져옵니다.
- 설정 이름은 프로젝트 런타임 `config`와 도메인 동작 `settings`를 구분합니다.
- 새 동작은 먼저 서비스 또는 포트 경계에 배치하고, 라우트는 호출과 응답 조립만 담당하게 합니다.

## 피해야 할 작업

- 라우트에서 `opennamu_forge.presentation.shared.func`의 예전 helper 묶음을 다시 가져오는 작업
- SQLModel row를 infrastructure 밖으로 반환하는 작업
- 라우트에서 직접 `subprocess`, thread, network I/O, DB session을 시작하는 작업
- `runtime_app.py`에 route 등록, scheduler, process loop를 직접 추가하는 작업
- legacy self-update HTTP route나 소스 트리 변경 로직을 되살리는 작업
