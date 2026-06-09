import html
import re

from opennamu_forge.presentation.dependencies import (
    get_html_filter_repository,
    get_user_setting_repository,
)
from opennamu_forge.presentation.shared.sql_dialect import ip_or_user


def do_user_name_check(user_name: str) -> int:
    html_filters = get_html_filter_repository()
    user_settings = get_user_setting_repository()

    if html.escape(user_name) != user_name:
        return 1

    if ip_or_user(user_name) == 1:
        return 1

    if "/" in user_name:
        return 1

    for name_filter in html_filters.list_by_kind("name"):
        if re.compile(name_filter.html, re.I).search(user_name):
            return 1

    if len(user_name) > 128:
        return 1

    if user_settings.data_exists("user_name", user_name):
        return 1

    if user_settings.id_exists(user_name):
        return 1

    return 0
