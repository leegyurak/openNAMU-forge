# 런타임과 GopenNAMU 스킬

시작 절차, 프로세스 생명주기, CLI, GopenNAMU 연동, scheduler, 서버 동작을 변경할 때 사용하는 절차입니다. 런타임 코드는 부팅 순서와 종료 순서가 중요하므로 작은 단위로 검증합니다.

## 확인 대상

- `opennamu_forge/presentation/runtime/`: 시작 옵션, 프로세스 제어, background job, GopenNAMU lifecycle
- `opennamu_forge/presentation/runtime_app.py`: 런타임 조립과 WSGI app 노출
- `opennamu_forge/cli.py`: CLI 진입점
- `opennamu_forge/application/version.py`: 런타임, schema, skin, GopenNAMU binary metadata
- `opennamu_forge/infrastructure/`: 외부 프로세스와 HTTP client adapter

## 구현 절차

1. config 생성, runtime DB 선택, migration, Flask setup, route registration, runtime hook, GopenNAMU lifecycle 순서를 먼저 확인합니다.
2. 프로세스 primitive는 `runtime/process_control.py`에 둡니다.
3. GopenNAMU 시작과 종료는 `runtime/gopennamu_process.py` 경계를 유지합니다.
4. startup seed와 default logic은 `runtime/startup_tasks.py`에 둡니다.
5. 네트워크 client 동작은 infrastructure adapter에 두고, presentation은 요청 context 조립까지만 담당합니다.
6. subprocess, psutil, requests, event loop, runtime context는 fake 또는 monkeypatch로 테스트합니다.

## GopenNAMU 계약

- `NAMU_GOLANGPORT` 계약을 유지합니다.
- readiness check는 `/compatible_api/test` 기준을 유지합니다.
- template bridge가 교체되기 전까지 `python_to_golang("post", path="template")` 동작을 유지합니다.
- 전체 라우트 위임에는 `python_to_golang("same")` 동작을 유지합니다.
- GopenNAMU 제거는 별도 마이그레이션 프로젝트로 취급합니다.

## 검증

- 런타임 단위 테스트와 GopenNAMU client/gateway 테스트를 실행합니다.
- 런타임 조립이나 프로세스 생명주기를 바꾸면 전체 pytest와 ty 검사를 실행합니다.
