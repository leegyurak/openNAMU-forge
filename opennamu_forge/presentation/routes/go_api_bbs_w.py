import sys

import flask

from opennamu_forge.presentation.golang_gateway import python_to_golang


async def api_bbs_w(sub_code = '', include_envelope = False):
    other_set = {}
    other_set['sub_code'] = sub_code

    data = await python_to_golang(sys._getframe().f_code.co_name, other_set)

    if include_envelope:
        return data
    else:
        return data["data"]

async def api_bbs_w_exter(sub_code = '', include_envelope = False):
    return flask.jsonify(await api_bbs_w(sub_code, include_envelope))
