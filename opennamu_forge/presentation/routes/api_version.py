from opennamu_forge.application.services.version_service import build_version_payload
from opennamu_forge.presentation.shared.func import flask
from opennamu_forge.presentation.dependencies import get_other_setting_repository
async def api_version(version_list):
    return flask.jsonify(build_version_payload(version_list, get_other_setting_repository()))
