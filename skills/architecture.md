# 아키텍처 변경 스킬

계층 구조, 모듈 경계, 라우트 분리, 서비스/저장소 이동, legacy 제거를 다룰 때 사용하는 절차입니다. 목적은 현재 아키텍처를 더 명확하게 만들되, 동작과 배포 경로를 불필요하게 흔들지 않는 것입니다.

## 먼저 확인할 것

- 요청이 동작 변경인지, 구조 정리인지, 테스트 보강인지 구분합니다.
- 같은 기능을 담당하는 기존 route, helper, service, repository, test를 모두 찾습니다.
- legacy 이름이나 경로를 제거할 때 import, template, static asset, 문서, 테스트 참조까지 함께 확인합니다.
- 변경이 WSGI startup, route registry, migration, GopenNAMU delegation에 영향을 주는지 확인합니다.

## 계층 결정 기준

- Flask request, session, redirect, template 선택은 presentation 계층에 둡니다.
- 권한, 설정, 문서 편집 정책처럼 오래 유지될 규칙은 application service에 둡니다.
- DB 모델, SQLModel session, query, 외부 client 구현은 infrastructure에 둡니다.
- 계층 사이 데이터는 DTO와 port를 사용합니다.
- 프로젝트 런타임 값은 `config`, 위키/사용자 동작 값은 `settings`로 이름을 구분합니다.

## 변경 절차

1. 현재 소유 계층을 확인하고 가장 작은 이동 단위를 정합니다.
2. 기존 동작을 보존하는 테스트를 먼저 추가하거나 갱신합니다.
3. provider, helper, mapper를 통해 의존 방향을 정리합니다.
4. route registry와 runtime composition은 한곳에서만 연결합니다.
5. legacy 경로 제거 시 새 경로로 참조가 모두 옮겨졌는지 `rg`로 확인합니다.
6. 문서와 agent 규칙을 새 구조에 맞게 갱신합니다.

## 주의할 경계

- `runtime_app.py`에 직접 route 등록, scheduler loop, process loop를 추가하지 않습니다.
- route module에서 raw SQL, DB session 생성, 외부 HTTP 호출을 하지 않습니다.
- `presentation/shared/func.py`에 새 공용 기능을 다시 모으지 않습니다.
- `presentation/rendering/` 밖에 rendering helper를 새로 만들지 않습니다.
- bootstrap table 제거, schema 변경, runtime 설정 변경은 migration 계획과 `.env.example` 동기화를 요구합니다.

## 검증

- 구조 변경 후 `rg`로 old path, old import, legacy naming을 확인합니다.
- 관련 단위 테스트를 먼저 실행한 뒤 route/runtime/shared 변경이면 전체 pytest를 실행합니다.
- public entrypoint가 바뀌면 README, docs, AGENTS, rules, skills를 함께 확인합니다.
