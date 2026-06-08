from .tool.func import *

async def api_version(version_list):
    with get_db_connect() as conn:
        update_setting = get_other_setting_repository().get("update")
        up_data = update_setting if update_setting in ['stable', 'beta', 'dev'] else 'stable'

        json_data = {
            "version" : version_list['r_ver'], 
            "db_version" : version_list['c_ver'],
            "skin_version" : version_list['s_ver'],
            "build" : up_data
        }

        return flask.jsonify(json_data)
