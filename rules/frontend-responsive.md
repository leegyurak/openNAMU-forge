# 프론트엔드와 Ringo 스킨

Ringo는 기본 스킨입니다. React/TypeScript source는 `views/ringo/src`, build asset은 `views/ringo/dist/assets`, 공용 static asset은 `views/main_css`를 사용합니다.

## 디자인 방향

- 위키 본문을 첫 번째 사용자 경험으로 둡니다.
- Header, drawer, document title block, document menu, body shell, sidebar/floating 영역, quick nav 구조를 유지합니다.
- SaaS dashboard처럼 조용하고 반복 사용에 강한 UI를 지향합니다.
- 장식적 hero, 과한 gradient, 큰 marketing card, one-note palette는 피합니다.
- 색상은 CSS variable과 token을 우선 사용하고, primary color는 `NAMU_THEME_COLOR` 경로를 따릅니다.
- panel/card radius는 작게 유지하고 border와 spacing으로 구조를 보여줍니다.

## 반응형 규칙

- desktop, tablet, mobile 폭에서 모두 사용 가능해야 합니다.
- page 전체 horizontal scroll에 primary content, nav, search, action tab, floating control을 의존시키지 않습니다.
- `max-width`, `width: 100%`, `flex-wrap`, `overflow-wrap`, `word-break`, stable dimensions, media query를 명시합니다.
- page width container에 `100vw`를 쓰지 않습니다. scrollbar overflow를 만들 수 있습니다.
- typography는 `vw`/`vh`로 scaling하지 않습니다. fixed/token 기반 font size를 사용합니다.
- 긴 문서 제목, 탭, 버튼, URL, code, table, math, rendered wiki content는 local container 안에서 wrap/scroll 처리합니다.
- floating control은 mobile에서 입력 영역이나 navigation을 가리지 않게 고정 크기와 위치 제약을 둡니다.

## Asset 규칙

- `views/ringo/index.html`은 `/forge/theme.css.cache_v1`을 runtime overrides보다 먼저 로드해야 합니다.
- Ringo build asset reference는 `/views/ringo/dist/assets/*.cache_v` 형태를 유지합니다.
- `views/main_css`는 favicon, logo, icon, route JS 등 공용 asset 영역이므로 default skin이 Ringo여도 제거하지 않습니다.
- source와 build asset을 같이 바꿨으면 둘이 같은 의도를 반영하는지 확인합니다.

## Theme Color

- `NAMU_THEME_COLOR`는 `/forge/theme.css.cache_v1`을 통해 `--forge-theme-color`로 노출됩니다.
- hex color만 허용하고 invalid value는 `#00a495`로 fallback합니다.
- 변수명, default, validation, CSS route를 바꾸면 `.env.example`, README, Docker docs, frontend smoke/theme test를 같이 갱신합니다.

## 검증

- layout CSS나 markup을 바꾸면 responsive invariant test를 추가/갱신합니다.
- browser tooling이 가능하면 최소 아래 viewport를 확인합니다:
  - desktop: `1366 x 768`
  - tablet: `768 x 1024`
  - mobile: `390 x 844`
- browser tooling이 없으면 정적 테스트와 CSS assertion을 추가하고, 미실행 사실을 명시합니다.
