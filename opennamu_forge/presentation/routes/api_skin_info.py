from opennamu_forge.presentation.encoding_helpers import json_loads
from opennamu_forge.presentation.dependencies import get_skin_info_client

from opennamu_forge.presentation.shared.func import (
    flask,
    load_skin,
    re,
    skin_check,
)

async def api_skin_info(name = ''):
    name = await skin_check() if name == '' else './views/' + name + '/index.html'
    skin_info_client = get_skin_info_client()

    if not flask.request.args.get('all', None):
        json_address = re.sub(r"(((?!\.|\/).)+)\.html$", "info.json", name)
        try:
            json_data = json_loads(open(json_address, encoding='utf8').read())
        except:
            json_data = None

        if json_data:
            return flask.jsonify(json_data)
        else:
            return flask.jsonify({}), 404
    else:
        a_data = {}
        d_link_data = {
            "ACME" : "https://raw.githubusercontent.com/openNAMU/openNAMU-Skin-ACME/master/info.json",
            "Liberty" : "https://raw.githubusercontent.com/openNAMU/openNAMU-Skin-Liberty/master/info.json",
            "Before Namu" : "https://raw.githubusercontent.com/openNAMU/openNAMU-Skin-Before_Namu/master/info.json"
        }

        for i in await load_skin(await skin_check(1), 1):
            json_address = re.sub(r"(((?!\.|\/).)+)\.html$", "info.json", './views/' + i + '/index.html')
            try:
                json_data = json_loads(open(json_address, encoding='utf8').read())
            except:
                json_data = None

            if json_data:
                if i == await skin_check(1):
                    json_data = {**json_data, **{ "main" : "true" }}

                if "info_link" in json_data:
                    info_link = json_data["info_link"]
                elif json_data["name"] in d_link_data:
                    info_link = d_link_data[json_data["name"]]
                else:
                    info_link = 0

                if info_link != 0:
                    latest_info = skin_info_client.fetch_latest_info(info_link)
                    if latest_info:
                        json_data = {**json_data, **{ "lastest_version" : {
                            "skin_ver" : latest_info.skin_ver
                        }}}

                a_data = {**a_data, **{ i : json_data }}

        return flask.jsonify(a_data)
