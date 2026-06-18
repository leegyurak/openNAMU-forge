# 테스트와 품질 스킬

테스트 보강, 커버리지 개선, 품질 게이트 검증에 사용하는 절차입니다. 변경 범위가 작더라도 기존 동작을 먼저 고정한 뒤 구현을 수정합니다.

## 적용 범위

- 회귀 테스트가 빠진 라우트, 헬퍼, 서비스, 저장소 동작
- 커버리지가 낮은 모듈의 분기, 예외, 경계값
- 런타임, 마이그레이션, 프론트 정적 자산 검증
- 리팩터링 전후 동작 보존 확인

## 기본 절차

1. 변경 대상과 가장 가까운 테스트 파일을 먼저 찾습니다.
2. 기존 동작을 설명하는 특성화 테스트를 추가합니다.
3. 외부 네트워크, 프로세스, 실제 DB 의존성은 통합 테스트가 아니면 fake, monkeypatch, 임시 세션으로 대체합니다.
4. 테스트 행렬은 `pytest.mark.parametrize`로 표현합니다.
5. 테스트 파일에는 명시적인 반복문과 컴프리헨션을 넣지 않습니다.
6. 공유 모듈을 건드렸다면 작은 테스트에서 시작해 전체 게이트까지 넓힙니다.

## 커버리지 보강 기준

- 정상 경로 하나만 검증하지 말고 실패 경로, 빈 값, 권한 없음, 기존 데이터 존재 여부를 함께 확인합니다.
- Flask 라우트는 URL, 상태 코드, 리다이렉트 위치, 템플릿/본문의 핵심 문자열을 검증합니다.
- 서비스는 DTO 입출력과 포트 호출을 검증하고, SQLModel row나 Flask 전역 객체에 의존하지 않게 합니다.
- 저장소는 영속화 결과와 쿼리 조건을 검증하되, 제어 흐름을 저장소 안에 늘리지 않습니다.
- 마이그레이션은 SQL dialect 변환과 bootstrap table 보존 여부를 별도 테스트로 확인합니다.
- 프론트 변경은 정적 검사와 렌더링 스모크 테스트를 함께 갱신합니다.

## 주요 명령

```bash
uv run --extra dev pytest
uv run --extra dev pytest tests/integration
uv run --extra dev ruff check app.py opennamu_forge migrations tests opennamu_forge/presentation/shared/sql_dialect.py
uv run --extra dev ty check app.py opennamu_forge/config opennamu_forge/application opennamu_forge/infrastructure opennamu_forge/presentation/flask_factory.py opennamu_forge/presentation/theme.py opennamu_forge/presentation/__init__.py opennamu_forge/presentation/url_converters.py opennamu_forge/presentation/dependencies.py opennamu_forge/presentation/response_helpers.py opennamu_forge/presentation/encoding_helpers.py opennamu_forge/presentation/captcha_helpers.py opennamu_forge/presentation/email_helpers.py opennamu_forge/presentation/file_helpers.py opennamu_forge/presentation/authorization_helpers.py opennamu_forge/presentation/identity_helpers.py opennamu_forge/presentation/text_helpers.py opennamu_forge/presentation/user_validation_helpers.py opennamu_forge/presentation/route_registry.py opennamu_forge/presentation/runtime migrations tests
uv run --extra dev python -m coverage run -m pytest
uv run --extra dev python -m coverage report --fail-under=90
```

## 정리

검증 뒤 생성된 `.coverage*`, `__pycache__`, 임시 DB 파일은 최종 상태에 남기지 않습니다.
