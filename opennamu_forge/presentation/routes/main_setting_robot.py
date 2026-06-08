from .tool.func import *

async def main_setting_robot():
    with get_db_connect() as conn:
        other_settings = get_other_setting_repository()

        if await acl_check('', 'owner_auth', '', '') == 1:
            return await re_error(conn, 0)

        data = other_settings.get('robot')
        default_value = other_settings.get('robot_default')
        if default_value != '':
            default_data = 'checked'
        else:
            default_data = ''
        
        if flask.request.method == 'POST':
            other_settings.set_many(
                {
                    'robot': flask.request.form.get('content', ''),
                    'robot_default': flask.request.form.get('default', ''),
                }
            )

            await acl_check(tool = 'owner_auth', memo = 'edit_set (robot)')

            return redirect(conn, '/setting/robot')
        else:
            return await render_template(
                'robots.txt',
                '''
                    <a href="/robots.txt">(''' + await get_lang('view') + ''')</a>
                    <hr class="main_hr">
                    <form method="post">
                        <textarea class="opennamu_forge_textarea_500 __ON_TEXTAREA__" name="content">''' + html.escape(data) + '''</textarea>
                        <hr class="main_hr">
                        <label class="__ON_CHECKLABEL__"><input class="__ON_CHECKBOX__" type="checkbox" name="default" ''' + default_data + '''> ''' + await get_lang('default') + '''</label>
                        <hr class="main_hr">
                        <button class="__ON_BUTTON__" id="opennamu_forge_save_button" type="submit">''' + await get_lang('save') + '''</button>
                    </form>
                ''',
                0,
                [['setting', await get_lang('return')]]
            )
