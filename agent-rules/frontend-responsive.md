# Frontend Responsive Design

Responsive behavior is non-negotiable for all HTML/CSS/JS changes.

## Required Baseline

- Every app or skin surface must work at desktop, tablet, and mobile widths.
- Mobile layouts must not depend on horizontal scrolling for primary content, navigation, search, action tabs, or floating controls.
- Use explicit responsive constraints such as `max-width`, `width: 100%`, `flex-wrap`, `overflow-wrap`, `min-height`, and stable control dimensions.
- Avoid `100vw` for page-width containers because it can create horizontal overflow with scrollbars. Prefer `width: 100%`.
- Do not use viewport-scaled typography. Font sizes must stay fixed or token-based, not `vw`/`vh`.
- Long document titles, menu labels, buttons, URLs, and rendered wiki content must wrap safely without overlapping neighboring UI.
- Floating controls must have fixed dimensions and must not cover primary input or navigation areas at mobile widths.

## Verification

- Add or update automated tests for responsive CSS invariants whenever changing skin markup or layout CSS.
- When an in-app browser is available, verify at minimum:
  - desktop: 1366 x 768
  - tablet: 768 x 1024
  - mobile: 390 x 844
- Capture screenshots or DOM/layout metrics for frontend layout changes when browser tooling is available.
- If browser tooling is unavailable, state that explicitly and rely on static tests, but do not skip adding responsive regression tests.
