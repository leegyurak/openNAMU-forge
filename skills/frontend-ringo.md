# 프론트엔드 Ringo 스킨 스킬

HTML, CSS, TypeScript, React, 정적 자산을 변경할 때 사용하는 절차입니다. Ringo는 문서 읽기와 편집이 중심인 위키 UI이므로 장식보다 가독성, 반응형 안정성, 기존 라우트 호환성을 우선합니다.

## 확인 대상

- `views/ringo/src`: 실제 스킨 소스와 스타일 토큰
- `views/ringo/index.html`: 빌드 진입점과 공통 HTML
- `views/ringo/dist`: 런타임에서 제공되는 빌드 결과
- `views/main_css`: 공유 자산과 라우트별 JavaScript 참조
- `tests/test_ringo_skin.py`, `tests/test_frontend_smoke.py`, `tests/test_responsive_design.py`: 정적/반응형 검증

## 구현 절차

1. 소스, dist, 테스트가 현재 어떤 파일명을 기대하는지 먼저 확인합니다.
2. header, drawer, 문서 제목, 문서 메뉴, 본문, sidebar, floating 영역, quick navigation 구조를 유지합니다.
3. 새 색상은 바로 추가하지 말고 CSS 변수와 기존 token을 먼저 사용합니다.
4. desktop, tablet, mobile 제약을 명시적으로 둡니다.
5. 레이아웃에 영향을 주는 변경은 정적 테스트와 반응형 테스트를 함께 갱신합니다.
6. 소스를 빌드했다면 `views/ringo/src`와 `views/ringo/dist/assets`가 같은 동작을 반영하는지 확인합니다.

## 디자인 규칙

- `/forge/theme.css.cache_v1`은 런타임 override보다 먼저 로드합니다.
- 기본 색상은 `--forge-theme-color`와 관련 변수를 사용합니다.
- 제목, 탭, 버튼, URL, 코드, 표, 수식, 렌더링된 위키 문서는 줄바꿈이 깨지지 않게 처리합니다.
- 페이지 폭 컨테이너에는 `100vw`를 사용하지 않습니다.
- viewport 기반 글자 크기 스케일링은 사용하지 않습니다.
- 카드형 UI는 반복 항목이나 실제 도구 영역에만 제한적으로 사용합니다.
- 문서 본문을 가리는 고정 요소, 겹치는 버튼, 숨겨지는 메뉴가 없도록 합니다.
- 기존 `views/main_css` 참조가 공유 asset이나 route JavaScript를 제공한다면 제거하지 않습니다.

## 검증

- 정적 변경은 관련 테스트 파일을 직접 실행합니다.
- 반응형 변경은 desktop, tablet, mobile 폭을 모두 확인합니다.
- 브라우저 도구를 사용할 수 있으면 핵심 화면 스크린샷으로 겹침, 잘림, 빈 화면 여부를 확인합니다.
