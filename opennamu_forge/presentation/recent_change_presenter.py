from __future__ import annotations

import html

from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.shared.sql_dialect import re


def recent_change_send_render(data):
    def send_render_href_replace(match):
        match = match.group(1)
        data_unescape = html.unescape(match)

        return '<a href="/w/' + url_pas(data_unescape) + '">' + match + "</a>"

    def send_render_link(match):
        link_main = match[2]
        link_main = link_main.replace('"', "&quot;")

        return match[1] + '<a href="' + link_main + '">' + link_main + "</a>"

    if data == "&lt;br&gt;" or data == "" or re.search(r"^ +$", data):
        data = "<br>"
    else:
        data = data.replace("javascript:", "")

        data = re.sub(r"( |^)(https?:\/\/(?:[^ ]+))", send_render_link, data)
        data = re.sub(r"&lt;a(?:(?:(?!&gt;).)*)&gt;((?:(?!&lt;\/a&gt;).)+)&lt;\/a&gt;", send_render_href_replace, data)

    return data
