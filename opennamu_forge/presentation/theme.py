from __future__ import annotations

import re

DEFAULT_THEME_COLOR = "#00a495"
THEME_COLOR_PATTERN = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


def normalize_theme_color(raw_color: str | None) -> str:
    if raw_color and THEME_COLOR_PATTERN.fullmatch(raw_color.strip()):
        return raw_color.strip().lower()

    return DEFAULT_THEME_COLOR


def build_theme_css(raw_color: str | None) -> str:
    theme_color = normalize_theme_color(raw_color)
    return (
        ":root {\n"
        f"    --forge-theme-color: {theme_color};\n"
        "    --forge-theme-color-strong: color-mix(in srgb, var(--forge-theme-color) 76%, #071f1b);\n"
        "    --forge-theme-color-muted: color-mix(in srgb, var(--forge-theme-color) 16%, transparent);\n"
        "    --forge-theme-color-surface: color-mix(in srgb, var(--forge-theme-color) 10%, #ffffff);\n"
        "}\n"
    )
