from opennamu_forge.presentation.text_helpers import cache_v
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    render_template,
)
async def list_user_check_submit(name = 'Test'):
    return await render_template(
        name,
        '' + \
            '<div id="opennamu_forge_list_user_check_submit"></div>' + \
            '<script defer src="/views/main_css/js/route/list_user_check_submit.js' + cache_v() + '"></script>' + \
            '<script>window.addEventListener("DOMContentLoaded", function() { opennamu_forge_list_user_check_submit(); });</script>' + \
        '',
        '(' + await get_lang('check') + ')',
        [['setting', await get_lang('return')]]
    )
