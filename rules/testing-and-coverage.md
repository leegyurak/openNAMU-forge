# 테스트와 커버리지

## 기본 명령

```bash
uv run --extra dev pytest
uv run --extra dev pytest tests/integration
uv run --extra dev python -m coverage run -m pytest
uv run --extra dev python -m coverage report --fail-under=90
```

## Coverage Target

- 전체 coverage는 90% 이상을 유지합니다.
- 새 Python code나 실질 변경 module은 focused characterization test를 둡니다.
- end-to-end로 어려운 module은 dependency boundary를 fake로 격리해서 테스트합니다.

## Test Design

- 테스트는 `tests/` 아래에 둡니다.
- integration test는 `tests/integration/` 아래에 둡니다.
- pytest 기반으로 작성하고 `unittest.TestCase`는 추가하지 않습니다.
- 테스트 함수명은 `test_` prefix를 유지하고 한국어로 작성합니다.
- case matrix는 `pytest.mark.parametrize`를 사용합니다.
- 테스트 파일에는 명시적 `for`/`while`, list/set/dict comprehension, generator expression을 쓰지 않습니다.
- 가능하면 `app.py` boot, 실제 DB, GopenNAMU process, network access 없이 테스트합니다.
- Flask request/session, repository, GopenNAMU client, subprocess, psutil, time은 fake를 사용해 경계를 테스트합니다.
- frontend layout 변경은 desktop/tablet/mobile responsive invariant test를 추가합니다.
- 작업 종료 전 `__pycache__`, `.coverage*`, 임시 DB artifact를 정리합니다.

## 현재 알려진 gap

- 실제 PostgreSQL/MySQL integration test는 로컬 기본 실행에서 skip될 수 있습니다.
- 제어된 DB와 GopenNAMU lifecycle을 포함한 full `app.py` boot test는 기본 unit path가 아닙니다.
- Docker Compose smoke test는 기본 local pytest에 포함되어 있지 않습니다.
- Alembic downgrade와 multi-revision upgrade path는 기본 suite에서 완전하게 다루지 않습니다.
