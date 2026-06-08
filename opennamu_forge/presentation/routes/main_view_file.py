from .tool.func import *

async def main_view_file(data = ''):
    with get_db_connect() as conn:
        if data == 'robots.txt':
            other_settings = get_other_setting_repository()
            if other_settings.get('robot_default') != '':
                return flask.Response(get_default_robots_txt(conn), mimetype = 'text/plain')
            else:
                robot_text = other_settings.get('robot')
                if robot_text != '':
                    return flask.Response(robot_text, mimetype = 'text/plain')
                else:
                    return flask.Response(get_default_robots_txt(conn), mimetype = 'text/plain')
        elif os.path.exists(data):
            if re.search(r'\.txt$', data, flags = re.I):
                return flask.send_from_directory('./', data, mimetype = 'text/plain')
            else:
                return flask.send_from_directory('./', data, mimetype = 'text/xml')
        else:
            return ''
