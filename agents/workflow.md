# 에이전트 작업 흐름

이 저장소에서 작업할 때는 작고 되돌리기 쉬운 변경을 기본값으로 둡니다.

## 작업 전

- 관련 `rules/`와 `skills/` 문서를 먼저 읽기.
- 주변 코드와 테스트를 확인한 뒤 구현 방식 정하기.
- `git status --short`로 기존 사용자 변경 확인하기.
- 관련 없는 파일, broad rewrite, 포맷 churn을 patch에 섞지 않기.

## 작업 중

- 기존 helper, service, port, DTO, repository, CSS token을 먼저 사용하기.
- 새 abstraction은 중복/복잡도를 실제로 줄일 때만 추가하기.
- 새 dependency는 기존 stack으로 해결이 어렵다는 근거가 있을 때만 추가하기.
- route 동작은 명시 요청이 없으면 보존하기.
- frontend 변경은 Ringo의 문서 중심 UI, 반응형 제약, CSS variable 체계를 유지하기.
- runtime 변경은 GopenNAMU lifecycle과 `NAMU_GOLANGPORT`를 유지하기.

## 검증

- 좁은 테스트부터 실행하고, 공유 동작을 건드렸으면 전체 gate를 실행하기.
- 실패나 skip은 숨기지 말고 원인과 범위를 남기기.
- coverage, `__pycache__`, 임시 DB 같은 생성물은 정리하기.

## 마무리 보고

- 무엇을 왜 바꿨는지 짧게 정리하기.
- 어떤 테스트/검증을 돌렸는지 명시하기.
- 남은 위험이나 미검증 영역이 있으면 바로 말하기.
