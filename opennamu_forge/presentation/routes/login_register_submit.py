from .tool.func import *

async def login_register_submit():
    with get_db_connect() as conn:
        session_reset_list = ['submit_id', 'submit_pw', 'submit_email']
        other_settings = get_other_setting_repository()
        user_settings = get_user_setting_repository()

        if not 'submit_id' in flask.session:
            for for_a in session_reset_list:
                flask.session.pop(for_a, None)

            return redirect(conn, '/register')

        data_que = other_settings.get("approval_question")
        if data_que == '':
            for for_a in session_reset_list:
                flask.session.pop(for_a, None)

            return redirect(conn, '/register')

        if do_user_name_check(conn, flask.session['submit_id']) == 1:
            for for_a in session_reset_list:
                flask.session.pop(for_a, None)
        
            return redirect(conn, '/register')

        if flask.request.method == 'POST':
            data_encode = other_settings.get("encode")

            user_app_data = {}
            user_app_data['id'] = flask.session['submit_id']
            user_app_data['pw'] = pw_encode(conn, flask.session['submit_pw'])
            user_app_data['encode'] = data_encode
            user_app_data['question'] = data_que
            user_app_data['answer'] = flask.request.form.get('answer', '')

            if 'submit_email' in flask.session:
                user_app_data['email'] = flask.session['submit_email']
            else:
                user_app_data['email'] = ''

            for for_a in session_reset_list:
                flask.session.pop(for_a, None)

            user_settings.upsert(user_app_data['id'], 'application', json_dumps(user_app_data))

            return await re_error(conn, 43)
        else:
            return await render_template(
                await get_lang('approval_question'),
                '''
                    <form method="post">
                        ''' + await get_lang('approval_question') + ' : ' + data_que + '''
                        <hr class="main_hr">
                        <input class="__ON_INPUT__" placeholder="''' + await get_lang('approval_question') + '''" name="answer">
                        <hr class="main_hr">
                        <button class="__ON_BUTTON__" type="submit">''' + await get_lang('save') + '''</button>
                    </form>
                ''',
                0,
                [['user', await get_lang('return')]]
            )
