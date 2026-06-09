from pathlib import Path

import pytest


def read_all_text(paths):
    return "\n".join(map(lambda path: path.read_text(encoding="utf-8"), paths))


JS_TEXT = read_all_text(Path("views/main_css/js").rglob("*.js"))
ROUTE_TEXT = read_all_text(Path("opennamu_forge/presentation/routes").rglob("*.py"))
RINGO_JS_TEXT = read_all_text(Path("views/ringo/js").rglob("*.js"))
RINGO_TEMPLATE_TEXT = Path("views/ringo/index.html").read_text(encoding="utf-8")
RINGO_CSS_TEXT = Path("views/ringo/css/main.css").read_text(encoding="utf-8")


@pytest.mark.parametrize(
    "function_name",
    (
        "opennamu_forge_do_render",
        "opennamu_forge_do_editor_preview",
        "opennamu_forge_do_url_encode",
        "opennamu_forge_do_footnote_spread",
        "opennamu_forge_do_category_spread",
        "opennamu_forge_file_preview",
        "opennamu_forge_get_thread",
    ),
)
def test_core_frontend_functions는_forge_namespace로_정의된다(function_name):
    assert f"function {function_name}" in JS_TEXT


@pytest.mark.parametrize(
    "function_name",
    (
        "opennamu_forge_do_editor_preview",
        "opennamu_forge_file_preview",
        "opennamu_forge_list_hidden_remove",
        "opennamu_forge_thread_delete",
    ),
)
def test_route_markup은_forge_frontend_functions를_호출한다(function_name):
    assert function_name in ROUTE_TEXT


def test_ringo_skin은_dynamic_theme_css를_로드한다():
    assert "/forge/theme.css.cache_v1" in RINGO_TEMPLATE_TEXT


@pytest.mark.parametrize(
    "legacy_text",
    (
        "function opennamu_",
        "function namu_",
        "2du.pythonanywhere.com",
    ),
)
def test_ringo_skin은_legacy_namespace와_문구를_사용하지_않는다(legacy_text):
    assert legacy_text not in RINGO_TEMPLATE_TEXT
    assert legacy_text not in RINGO_JS_TEXT


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
def test_ringo_skin은_css_variable_design_token을_사용한다(css_variable):
    assert css_variable in RINGO_CSS_TEXT
