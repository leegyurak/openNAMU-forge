import os

import flask

from opennamu_forge.presentation.dependencies import get_other_setting_repository
from opennamu_forge.presentation.file_helpers import get_default_robots_txt
from opennamu_forge.presentation.shared.sql_dialect import re


async def main_view_file(data = ''):
    if data == 'robots.txt':
        other_settings = get_other_setting_repository()
        if other_settings.get('robot_default') != '':
            return flask.Response(get_default_robots_txt(), mimetype = 'text/plain')
        else:
            robot_text = other_settings.get('robot')
            if robot_text != '':
                return flask.Response(robot_text, mimetype = 'text/plain')
            else:
                return flask.Response(get_default_robots_txt(), mimetype = 'text/plain')
    elif os.path.exists(data):
        if re.search(r'\.txt$', data, flags = re.I):
            return flask.send_from_directory('./', data, mimetype = 'text/plain')
        else:
            return flask.send_from_directory('./', data, mimetype = 'text/xml')
    else:
        return ''
