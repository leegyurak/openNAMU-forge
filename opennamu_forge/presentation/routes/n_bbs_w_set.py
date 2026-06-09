from opennamu_forge.presentation.dependencies import get_bbs_repository
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    redirect,
    render_template,
)
from opennamu_forge.presentation.text_helpers import cache_v


async def bbs_w_set(bbs_num = ''):
    bbs = get_bbs_repository()

    bbs_name = bbs.get_setting(str(bbs_num), "bbs_name")
    if bbs_name == "":
        return redirect('/bbs/main')

    bbs_num_str = str(bbs_num)

    return await render_template(
        await get_lang('bbs_set'),
        '' + \
            '<div id="opennamu_forge_bbs_w_set"></div>' + \
            '<script defer src="/views/main_css/js/route/bbs_w_set.js' + cache_v() + '"></script>' + \
            '<script>window.addEventListener("DOMContentLoaded", function() { opennamu_forge_bbs_w_set(); });</script>' + \
        '',
        '(' + bbs_name + ')',
        [['bbs/in/' + bbs_num_str, await get_lang('return')]]
    )
