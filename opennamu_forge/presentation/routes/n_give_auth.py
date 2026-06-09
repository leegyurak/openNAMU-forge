from opennamu_forge.presentation.text_helpers import cache_v
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    render_template,
)
async def give_auth(user_name = ''):
    if user_name == '':
        user_name = await get_lang('authorize')
        sub = 0
    else:
        sub = '(' + await get_lang('authorize') + ')'

    return await render_template(
        user_name,
        '' + \
            '<div id="opennamu_forge_give_auth"></div>' + \
            '<script defer src="/views/main_css/js/route/give_auth.js' + cache_v() + '"></script>' + \
            '<script>window.addEventListener("DOMContentLoaded", function() { opennamu_forge_give_auth(); });</script>' + \
        '',
        sub,
        [['manager', await get_lang('return')]]
    )
