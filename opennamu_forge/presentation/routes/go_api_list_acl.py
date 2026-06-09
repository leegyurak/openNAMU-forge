import sys

import flask

from opennamu_forge.presentation.golang_gateway import python_to_golang


async def api_list_acl(data_type = ''):
    other_set = {}
    other_set = data_type

    return flask.jsonify(await python_to_golang(sys._getframe().f_code.co_name, other_set))
