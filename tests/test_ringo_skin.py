from pathlib import Path

import pytest

SKIN_ROOT = Path("views/ringo")
SKIN_TEMPLATE = SKIN_ROOT / "index.html"
SKIN_INFO = SKIN_ROOT / "info.json"
SKIN_DIST_CSS = SKIN_ROOT / "dist" / "assets" / "main.css"
SKIN_DIST_RUNTIME_OVERRIDES_CSS = SKIN_ROOT / "dist" / "assets" / "runtime-overrides.css"
SKIN_DIST_JS = SKIN_ROOT / "dist" / "assets" / "main.js"

SKIN_PACKAGE = SKIN_ROOT / "package.json"
SKIN_PACKAGE_LOCK = SKIN_ROOT / "package-lock.json"
SKIN_VITE_CONFIG = SKIN_ROOT / "vite.config.ts"
SKIN_TS_CONFIG = SKIN_ROOT / "tsconfig.json"
SKIN_TS_ENTRY = SKIN_ROOT / "src" / "main.tsx"
SKIN_TOKENS_CSS = SKIN_ROOT / "src" / "styles" / "tokens.css"
SKIN_GLOBAL_CSS = SKIN_ROOT / "src" / "styles" / "global.css"
SKIN_DOC_CONTENT_CSS = SKIN_ROOT / "src" / "styles" / "document-content.css"
SKIN_HEADER_CSS = SKIN_ROOT / "src" / "components" / "header" / "Header.module.css"
SKIN_DOCUMENT_CSS = SKIN_ROOT / "src" / "components" / "document" / "DocumentView.module.css"
SKIN_SIDEBAR_CSS = SKIN_ROOT / "src" / "components" / "sidebar" / "FloatingSidebar.module.css"
SKIN_NAV_CSS = SKIN_ROOT / "src" / "components" / "nav" / "QuickNav.module.css"
SKIN_DRAWER_CSS = SKIN_ROOT / "src" / "components" / "drawer" / "Drawer.module.css"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_ringo_skin_은_필수_파일을_가진다():
    assert SKIN_TEMPLATE.is_file()
    assert SKIN_INFO.is_file()


def test_ringo_skin_은_빌드된_정적_자산을_가진다():
    assert SKIN_DIST_CSS.is_file()
    assert SKIN_DIST_RUNTIME_OVERRIDES_CSS.is_file()
    assert SKIN_DIST_JS.is_file()


def test_ringo_skin_은_react_ts_소스를_유지한다():
    package_text = read_text(SKIN_PACKAGE)
    assert '"react"' in package_text
    assert '"react-dom"' in package_text
    assert '"typescript"' in package_text
    assert SKIN_TS_CONFIG.is_file()
    assert SKIN_TS_ENTRY.is_file()


def test_ringo_skin_은_vite_를_사용하지_않는다():
    package_text = read_text(SKIN_PACKAGE)
    tsconfig_text = read_text(SKIN_TS_CONFIG)
    assert not SKIN_VITE_CONFIG.exists()
    assert not SKIN_PACKAGE_LOCK.exists()
    assert '"vite"' not in package_text
    assert "@vitejs/plugin-react" not in package_text
    assert "vite/client" not in tsconfig_text


def test_ringo_skin_template_은_react_root_를_노출한다():
    template_text = read_text(SKIN_TEMPLATE)
    assert 'id="ringo-app-root"' in template_text


@pytest.mark.parametrize(
    "island_id",
    (
        "ringo-app-island-license",
        "ringo-app-island-pre-body",
        "ringo-app-island-body",
        "ringo-app-island-post-body",
        "ringo-app-island-sidebar-override",
        "ringo-app-island-document-menu",
        "ringo-app-island-added-menu",
        "ringo-app-island-labels",
    ),
)
def test_ringo_skin_template_은_hydration_islands_를_제공한다(island_id):
    template_text = read_text(SKIN_TEMPLATE)
    assert f'id="{island_id}"' in template_text


@pytest.mark.parametrize(
    "meta_name",
    (
        "ringo-app:doc-title",
        "ringo-app:doc-sub-title",
        "ringo-app:doc-last-edit",
        "ringo-app:wiki-name",
        "ringo-app:user-name",
        "ringo-app:user-auth",
        "ringo-app:user-login",
        "ringo-app:user-alarm-count",
        "ringo-app:user-path",
    ),
)
def test_ringo_skin_template_은_초기_상태_meta_를_가진다(meta_name):
    template_text = read_text(SKIN_TEMPLATE)
    assert f'name="{meta_name}"' in template_text


def test_ringo_skin_은_dynamic_theme_css_를_로드한다():
    template_text = read_text(SKIN_TEMPLATE)
    assert "/forge/theme.css.cache_v1" in template_text


def test_ringo_skin_runtime_overrides는_dynamic_theme_css_뒤에_로드된다():
    template_text = read_text(SKIN_TEMPLATE)
    theme_index = template_text.index("/forge/theme.css.cache_v1")
    overrides_index = template_text.index("/views/ringo/dist/assets/runtime-overrides.css.cache_v")
    assert theme_index < overrides_index


def test_ringo_skin_은_빌드된_정적_자산을_cache_suffix_와_함께_참조한다():
    template_text = read_text(SKIN_TEMPLATE)
    assert "/views/ringo/dist/assets/main.css.cache_v" in template_text
    assert "/views/ringo/dist/assets/runtime-overrides.css.cache_v" in template_text
    assert "/views/ringo/dist/assets/main.js.cache_v" in template_text


def test_ringo_skin_static_bundle은_browser_process_shim을_포함한다():
    js_text = read_text(SKIN_DIST_JS)
    assert 'var process = { env: { NODE_ENV: "production" } };' in js_text


@pytest.mark.parametrize(
    "css_variable",
    (
        "--forge-theme-color",
        "--forge-bg",
        "--forge-surface",
        "--forge-text",
        "--forge-line",
    ),
)
def test_ringo_skin_은_css_variable_design_token_을_사용한다(css_variable):
    tokens_text = read_text(SKIN_TOKENS_CSS)
    assert css_variable in tokens_text


@pytest.mark.parametrize(
    "namu_variable",
    (
        "--namu-page-bg",
        "--namu-panel-bg",
        "--namu-header-bg",
        "--namu-border",
        "--namu-info-bg",
    ),
)
def test_ringo_skin_은_namuwiki_design_tokens_를_정의한다(namu_variable):
    tokens_text = read_text(SKIN_TOKENS_CSS)
    assert namu_variable in tokens_text


def test_ringo_skin_은_namuwiki_스타일_문서_콘텐츠_규칙을_가진다():
    document_css = read_text(SKIN_DOC_CONTENT_CSS)
    assert ".opennamu_forge_main h1" in document_css
    assert ".opennamu_forge_TOC" in document_css
    assert ".opennamu_forge_footnote" in document_css


def test_ringo_skin_은_namuwiki_스타일_헤딩_경계를_가진다():
    document_css = read_text(SKIN_DOC_CONTENT_CSS)
    assert "border-bottom: 1px solid var(--namu-border)" in document_css
    assert ".opennamu_forge_main h1::before" not in document_css


def test_ringo_skin_header는_theme_color를_background로_쓰지_않는다():
    tokens_text = read_text(SKIN_TOKENS_CSS)
    header_css = read_text(SKIN_HEADER_CSS)
    assert "--namu-header-bg: #008275" not in tokens_text
    assert "--namu-header-bg: #126b60" not in tokens_text
    assert "border-bottom: 2px solid var(--forge-theme-color)" in header_css


def test_ringo_skin_document는_pc에서_left_aligned다():
    document_css = read_text(SKIN_DOCUMENT_CSS)
    assert "margin: 16px 0 0;" in document_css
    assert "margin: 16px auto 0" not in document_css


def test_ringo_skin_은_edit_actionbar_스타일을_가진다():
    document_css = read_text(SKIN_DOC_CONTENT_CSS)
    runtime_css = read_text(SKIN_DIST_RUNTIME_OVERRIDES_CSS)
    assert ".opennamu_forge_edit_actionbar" in document_css
    assert ".opennamu_forge_edit_action_add" in document_css
    assert ".opennamu_forge_edit_actionbar" in runtime_css


@pytest.mark.parametrize(
    "css_path",
    (
        SKIN_HEADER_CSS,
        SKIN_DOCUMENT_CSS,
        SKIN_SIDEBAR_CSS,
        SKIN_NAV_CSS,
        SKIN_DRAWER_CSS,
    ),
    ids=("header", "document-view", "floating-sidebar", "quick-nav", "drawer"),
)
def test_ringo_skin_레이아웃_컴포넌트는_mobile_breakpoint_를_가진다(css_path):
    css_text = read_text(css_path)
    assert "@media (max-width:" in css_text


@pytest.mark.parametrize(
    "css_path",
    (
        SKIN_HEADER_CSS,
        SKIN_DOCUMENT_CSS,
        SKIN_SIDEBAR_CSS,
        SKIN_DRAWER_CSS,
    ),
    ids=("header", "document-view", "floating-sidebar", "drawer"),
)
def test_ringo_skin_레이아웃은_full_viewport_width_를_쓰지_않는다(css_path):
    css_text = read_text(css_path)
    assert "width: 100vw" not in css_text
    assert "100vh" not in css_text


@pytest.mark.parametrize(
    "css_path",
    (
        SKIN_DOC_CONTENT_CSS,
        SKIN_DOCUMENT_CSS,
    ),
    ids=("document-content", "document-view"),
)
def test_ringo_skin_문서_콘텐츠는_safe_wrap_규칙을_가진다(css_path):
    assert "overflow-wrap: anywhere" in read_text(css_path)


def test_ringo_skin_template_은_skin_set_화면_링크를_제공한다():
    template_text = read_text(SKIN_TEMPLATE)
    assert "skin_setting" in template_text


def test_legacy_skin_directory는_남겨두지_않는다():
    skin_paths = filter(
        lambda path: path.is_dir() and (path / "index.html").is_file(),
        Path("views").iterdir(),
    )
    skin_dirs = tuple(sorted(map(lambda path: path.name, skin_paths)))

    assert skin_dirs == ("ringo",)
    assert not Path("views/legacy").exists()
    assert not Path("views/default").exists()


def test_ringo_skin_global_css_는_pretendard_와_한글_폰트_폴백_을_정의한다():
    global_css = read_text(SKIN_GLOBAL_CSS)
    assert "Pretendard" in global_css
    assert "Apple SD Gothic Neo" in global_css


def test_ringo_skin_은_좌측_drawer_와_hamburger_를_가진다():
    drawer_css = read_text(SKIN_DRAWER_CSS)
    header_css = read_text(SKIN_HEADER_CSS)
    assert ".panel" in drawer_css
    assert "translateX" in drawer_css
    assert ".hamburger" in header_css


def test_ringo_skin_은_dark_header_palette_를_가진다():
    header_css = read_text(SKIN_HEADER_CSS)
    assert "var(--namu-header-bg)" in header_css


@pytest.mark.parametrize(
    "legacy_text",
    (
        "2du.pythonanywhere.com",
        "function opennamu_",
        "function namu_",
    ),
)
def test_ringo_skin_은_legacy_네임스페이스를_사용하지_않는다(legacy_text):
    template_text = read_text(SKIN_TEMPLATE)
    assert legacy_text not in template_text
