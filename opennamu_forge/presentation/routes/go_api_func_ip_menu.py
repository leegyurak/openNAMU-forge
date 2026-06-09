import sys

import flask

from opennamu_forge.presentation.golang_gateway import python_to_golang


async def api_func_ip_menu(ip = "Test", option = ""):
    other_set = {}
    other_set["ip"] = ip
    other_set["option"] = option

    return flask.jsonify(await python_to_golang(sys._getframe().f_code.co_name, other_set))
