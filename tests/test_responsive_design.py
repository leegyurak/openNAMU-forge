from pathlib import Path

import pytest

RINGO_CSS_TEXT = Path("views/ringo/css/main.css").read_text(encoding="utf-8")


@pytest.mark.parametrize(
    "required_css",
    (
        "@media screen and (max-width: 1000px)",
        "section {\n        width: 100%;",
        "aside {\n        float: none;\n        width: 100%;",
        "header#main span#right {\n        float: none;\n        display: flex;\n        flex-wrap: wrap;",
        "header#main form.only_mobile {\n        line-height: 1;\n        width: 100%;",
        "input.only_mobile.search {\n    display: inline-block;\n    width: calc(100% - 82px);",
        ".top_cel_in {\n        left: 0;\n        right: auto;",
        ".change_space,\n.opennamu_forge_main {\n    overflow-wrap: anywhere;",
    ),
)
def test_ringo_css는_responsive_invariant를_유지한다(required_css):
    assert required_css in RINGO_CSS_TEXT


@pytest.mark.parametrize(
    "forbidden_css",
    (
        "width: 100vw",
        "font-size: 1vw",
        "font-size: 2vw",
        "font-size: 3vw",
        "letter-spacing: -",
    ),
)
def test_ringo_css는_responsive_안티패턴을_사용하지_않는다(forbidden_css):
    assert forbidden_css not in RINGO_CSS_TEXT
