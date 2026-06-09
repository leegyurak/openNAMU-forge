from opennamu_forge.presentation.file_helpers import load_image_url
from opennamu_forge.presentation.shared.func import (
    flask,
    os,
)

async def api_image_view(name = 'Test'):
    if os.path.exists(os.path.join(load_image_url(), name)):
        return flask.jsonify({ "exist" : "1" })
    else:
        return flask.jsonify({})