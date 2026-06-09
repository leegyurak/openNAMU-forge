from pathlib import Path

import pytest

from opennamu_forge.presentation.theme import DEFAULT_THEME_COLOR, build_theme_css, normalize_theme_color


@pytest.mark.parametrize(
    ("raw_color", "expected_color"),
    (
        ("#00A495", "#00a495"),
        (" #abc ", "#abc"),
        ("rgb(0, 0, 0)", DEFAULT_THEME_COLOR),
        ("red", DEFAULT_THEME_COLOR),
        ("#nothex", DEFAULT_THEME_COLOR),
        (None, DEFAULT_THEME_COLOR),
    ),
)
def test_theme_color는_hex만_허용한다(raw_color, expected_color):
    assert normalize_theme_color(raw_color) == expected_color


def test_theme_css는_css_variable을_생성한다():
    css = build_theme_css("#123456")

    assert "--forge-theme-color: #123456;" in css
    assert "--forge-theme-color-strong:" in css


@pytest.mark.parametrize(
    "path",
    (
        ".env.example",
        "README.md",
        "docs/docker.md",
        "agent-rules/frontend-responsive.md",
    ),
)
def test_theme_color_env는_문서화되어_있다(path):
    assert "NAMU_THEME_COLOR" in Path(path).read_text(encoding="utf-8")
