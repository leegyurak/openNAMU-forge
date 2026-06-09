from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.dependencies import get_bbs_repository
from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    render_template,
)


async def bbs_w_tool(bbs_num = '', post_num = ''):
    bbs = get_bbs_repository()

    data = ''
    
    bbs_num_str = str(bbs_num)
    post_num_str = str(post_num)
    
    data += '''
        <h2>''' + await get_lang('tool') + '''</h2>
        <ul>
            <li><a href="/bbs/raw/''' + url_pas(bbs_num_str) + '/' + url_pas(post_num_str) + '">' + await get_lang('raw') + '''</a></li>
        </ul>
    '''

    if await acl_check('', 'bbs_auth', '', '') != 1:
        pinned = await get_lang('pinned') if not bbs.is_pinned(bbs_num_str, post_num_str) else await get_lang('pinned_release')

        data += '''
            <h3>''' + await get_lang('admin') + '''</h3>
            <ul>
                <!-- <li><a href="/bbs/blind/''' + url_pas(bbs_num_str) + '/' + url_pas(post_num_str) + '">' + await get_lang('hide') + '''</a></li> -->
                <li><a href="/bbs/pinned/''' + url_pas(bbs_num_str) + '/' + url_pas(post_num_str) + '">' + pinned + '''</a></li>
            </ul>
        '''

        data += '''
            <h3>''' + await get_lang('owner') + '''</h2>
            <ul>
                <li><a href="/bbs/delete/''' + url_pas(bbs_num_str) + '/' + url_pas(post_num_str) + '">' + await get_lang('delete') + '''</a></li>
            </ul>
        '''

    return await render_template(
        await get_lang('bbs_post_tool'),
        data,
        0,
        [['bbs/w/' + url_pas(bbs_num_str) + '/' + url_pas(post_num_str), await get_lang('return')]]
    )
