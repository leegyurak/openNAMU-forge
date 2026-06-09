from opennamu_forge.presentation.shared.func import (
    flask,
    python_to_golang,
    sys,
)

async def api_bbs_w_comment(sub_code = '', tool = "", include_envelope = False):
    other_set = {}
    other_set["sub_code"] = sub_code
    other_set["tool"] = tool

    data = await python_to_golang(sys._getframe().f_code.co_name, other_set)
    if include_envelope:
        return data
    else:
        return data["data"]

async def api_bbs_w_comment_exter(sub_code = '', tool = "", include_envelope = False):
    return flask.jsonify(await api_bbs_w_comment(sub_code, tool, include_envelope))
