from __future__ import annotations

import os

from opennamu_forge.presentation.dependencies import get_other_setting_repository
from opennamu_forge.presentation.response_helpers import load_domain


def load_image_url() -> str:
    return get_other_setting_repository().get("image_where", default=os.path.join("data", "images"))


def get_default_robots_txt() -> str:
    data = (
        "User-agent: *\n"
        "Disallow: /\n"
        "Allow: /$\n"
        "Allow: /w/\n"
        "Allow: /bbs/w/\n"
        "Allow: /sitemap.xml$\n"
        "Allow: /sitemap_*.xml$"
    )

    if os.path.exists("sitemap.xml"):
        data += "\nSitemap: " + load_domain("full") + "/sitemap.xml"

    return data
