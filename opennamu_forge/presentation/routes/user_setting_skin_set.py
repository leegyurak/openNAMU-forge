import flask

from opennamu_forge.presentation.dependencies import (
    get_other_setting_repository,
    get_user_setting_repository,
)
from opennamu_forge.presentation.response_helpers import re_error
from opennamu_forge.presentation.shared.sql_dialect import ip_check


async def user_setting_skin_set():
    data = flask.make_response(await re_error(5))

    main_data = get_other_setting_repository().get("language")
    user_data = get_user_setting_repository().get(ip_check(), "lang", default=main_data)

    data.set_cookie('language', main_data)
    data.set_cookie('user_language', user_data)

    return data
