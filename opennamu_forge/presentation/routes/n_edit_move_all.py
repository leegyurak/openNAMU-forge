from opennamu_forge.presentation.text_helpers import cache_v
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    render_template,
)
async def edit_move_all():
    return await render_template(
        await get_lang('multiple_move'),
        '' + \
            '<div id="opennamu_forge_edit_move_all"></div>' + \
            '<script defer src="/views/main_css/js/route/edit_move_all.js' + cache_v() + '"></script>' + \
            '<script>window.addEventListener("DOMContentLoaded", function() { opennamu_forge_edit_move_all(); });</script>' + \
        '',
        0,
        [['other', await get_lang('return')]]
    )
