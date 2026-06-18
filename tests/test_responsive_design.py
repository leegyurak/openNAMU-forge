from itertools import product
from pathlib import Path

import pytest

SKIN_LAYOUT_CSS = (
    Path("views/ringo/src/components/header/Header.module.css"),
    Path("views/ringo/src/components/document/DocumentView.module.css"),
    Path("views/ringo/src/components/sidebar/FloatingSidebar.module.css"),
    Path("views/ringo/src/components/nav/QuickNav.module.css"),
    Path("views/ringo/src/components/drawer/Drawer.module.css"),
)
SKIN_CONTENT_CSS = (
    Path("views/ringo/src/styles/document-content.css"),
    Path("views/ringo/src/components/document/DocumentView.module.css"),
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


@pytest.mark.parametrize("css_path", SKIN_LAYOUT_CSS, ids=lambda p: p.stem)
def test_ringo_layout_css는_mobile_breakpoint를_제공한다(css_path):
    text = read_text(css_path)
    assert "@media (max-width:" in text


@pytest.mark.parametrize("css_path", SKIN_LAYOUT_CSS, ids=lambda p: p.stem)
def test_ringo_layout_css는_full_viewport_width를_쓰지_않는다(css_path):
    text = read_text(css_path)
    assert "width: 100vw" not in text


VW_FORBIDDEN = ("font-size: 1vw", "font-size: 2vw", "font-size: 3vw")
VW_TARGETS = SKIN_LAYOUT_CSS + SKIN_CONTENT_CSS


@pytest.mark.parametrize(
    ("css_path", "forbidden"),
    tuple(product(VW_TARGETS, VW_FORBIDDEN)),
    ids=lambda value: getattr(value, "stem", value),
)
def test_ringo_skin은_viewport_scaled_typography를_사용하지_않는다(css_path, forbidden):
    assert forbidden not in read_text(css_path)


@pytest.mark.parametrize("css_path", SKIN_CONTENT_CSS, ids=lambda p: p.stem)
def test_ringo_content_css는_safe_wrap_규칙을_가진다(css_path):
    assert "overflow-wrap: anywhere" in read_text(css_path)
