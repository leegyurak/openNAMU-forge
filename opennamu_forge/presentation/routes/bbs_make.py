from .tool.func import *

async def bbs_make():   
    with get_db_connect() as conn:
        bbs = get_bbs_repository()

        if await acl_check('', 'owner_auth', '', '') == 1:
            return await re_error(conn, 3)
        
        if flask.request.method == 'POST':
            latest_board_id = bbs.latest_board_id()
            bbs_num = str(latest_board_id + 1) if latest_board_id is not None else '1'
            bbs_name = flask.request.form.get('bbs_name', 'test')
            bbs_type = flask.request.form.get('bbs_type', 'comment')
            bbs_type = bbs_type if bbs_type in ['comment', 'thread'] else 'comment'

            bbs.add_setting(bbs_num, 'bbs_name', bbs_name)
            bbs.add_setting(bbs_num, 'bbs_type', bbs_type)

            return redirect(conn, '/bbs/main')
        else:
            return await render_template(
                await get_lang('bbs_make'),
                '''
                    <form method="post">
                        <input class="__ON_INPUT__" placeholder="''' + await get_lang('bbs_name') + '''" name="bbs_name">
                        <hr class="main_hr">
                        
                        <span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" name="bbs_type">
                            <option value="comment">''' + await get_lang('comment_base') + '''</option>
                            <option value="thread">''' + await get_lang('thread_base') + '''</option>
                        </select></span>
                        <hr class="main_hr">
                        
                        <button class="__ON_BUTTON__" type="submit">''' + await get_lang('save') + '''</button>
                    </form>
                ''',
                0,
                [['bbs/main', await get_lang('return')]]
            )
