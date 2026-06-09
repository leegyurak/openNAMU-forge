from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.shared.func import (
    flask,
    html,
    re_error,
)
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    redirect,
    render_template,
)
from opennamu_forge.presentation.dependencies import get_admin_repository
async def give_admin_groups(name = 'test'):
    admin = get_admin_repository()

    acl_name_list = [
        [1, 'owner', await get_lang('owner_authority')],
            [2, '', await get_lang('all_function_authority')],
            [2, 'admin', await get_lang('admin_authority')],
                [3, 'ban', await get_lang('ban_authority')],
                    [4, '', await get_lang('admin_default_feature_authority')],
                [3, 'toron', await get_lang('discussion_authority')],
                    [4, '', await get_lang('admin_default_feature_authority')],
                [3, 'check', await get_lang('user_analyze_authority')],
                    [4, 'view_user_watchlist', await get_lang('view_user_watchlist_authority')],
                    [4, '', await get_lang('user_check_authority')],
                    [4, '', await get_lang('admin_default_feature_authority')],
                [3, 'acl', await get_lang('document_acl_authority')],
                    [4, '', await get_lang('admin_default_feature_authority')],
                [3, 'hidel', await get_lang('history_hide_authority')],
                    [4, '', await get_lang('admin_default_feature_authority')],
                [3, 'give', await get_lang('authorization_authority')],
                    [4, '', await get_lang('admin_default_feature_authority')],
                [3, 'bbs', await get_lang('bbs_management_authority')],
                    [4, '', await get_lang('admin_default_feature_authority')],
                [3, 'vote_fix', await get_lang('vote_management_authority')],
                    [4, '', await get_lang('admin_default_feature_authority')],
                [3, 'admin_default_feature', await get_lang('admin_default_feature_authority')],
                    [4, 'doc_watch_list_view', await get_lang('doc_watch_list_view_authority')],
                    [4, 'treat_as_admin', await get_lang('treat_as_admin_authority')],
                    [4, 'view_hide_user_name', await get_lang('view_hide_user_name_authority')],
                    [4, 'user_name_bold', await get_lang('user_name_bold_authority')],
                    [4, 'multiple_upload', await get_lang('multiple_upload_authority')],
                    [4, 'slow_edit_pass', await get_lang('slow_edit_pass_authority')],
                    [4, 'edit_bottom_compulsion_pass', await get_lang('edit_bottom_compulsion_pass_authority')],
                    [4, 'edit_filter_pass', await get_lang('edit_filter_pass_authority')],
                    [4, '', await get_lang('user_authority')],
        [1, 'user', await get_lang('user_authority')],
            [2, 'captcha_pass', await get_lang('captcha_pass_authority')],
            [2, 'ip', await get_lang('ip_authority')],
                [3, 'document', await get_lang('document_authority')],
                    [4, 'edit', await get_lang('edit_authority')],
                        [5, '', await get_lang('view_authority')],
                    [4, 'edit_request', await get_lang('edit_request_authority')],
                        [5, '', await get_lang('view_authority')],
                    [4, 'move', await get_lang('move_authority')],
                        [5, '', await get_lang('view_authority')],
                    [4, 'new_make', await get_lang('new_make_authority')],
                        [5, '', await get_lang('view_authority')],
                    [4, 'delete', await get_lang('delete_authority')],
                        [5, '', await get_lang('view_authority')],
                    [4, 'view', await get_lang('view_authority')],
                [3, 'discuss', await get_lang('discuss_authority')],
                    [4, 'discuss_make_new_thread', await get_lang('discuss_make_new_thread_authority')],
                        [5, '', await get_lang('discuss_view_authority')],
                    [4, 'discuss_view', await get_lang('discuss_view_authority')],
                [3, 'upload', await get_lang('upload_authority')],
                [3, 'vote', await get_lang('vote_authority')],
                [3, 'bbs_use', await get_lang('bbs_authority')],
                    [4, 'bbs_edit', await get_lang('bbs_edit_authority')],
                        [5, '', await get_lang('bbs_view_authority')],
                    [4, 'bbs_comment', await get_lang('bbs_comment_authority')],
                        [5, '', await get_lang('bbs_view_authority')],
                    [4, 'bbs_view', await get_lang('bbs_view_authority')],
                [3, 'captcha_one_check_five_pass', await get_lang('captcha_one_check_five_pass_authority')],
                [3, 'edit_filter_view', await get_lang('edit_filter_view_authority')],
                [3, 'nothing', await get_lang('nothing_authority')]
    ]

    if html.escape(name) != name:
        return await re_error(48)

    if flask.request.method == 'POST':
        if await acl_check(tool = 'owner_auth', memo = 'auth list add (' + name + ')') == 1:
            return await re_error(3)

        acl_values = tuple([for_a[1] for for_a in acl_name_list if flask.request.form.get(for_a[1], 0) != 0] + ['nothing'])
        admin.set_group_acls(name, acl_values)

        return redirect('/auth/list/add/' + url_pas(name))
    else:
        state = 'disabled' if await acl_check('', 'owner_auth', '', '') == 1 else ''

        acl_list = admin.list_group_acls(name)

        data = '<ul>'
        for for_a in acl_name_list:                
            checked = ''
            if for_a[1] in acl_list:
                checked = 'checked'
                
            choice = '<label class="__ON_CHECKLABEL__"><input class="__ON_CHECKBOX__" type="checkbox" ' + state + ' name="' + for_a[1] + '" ' + checked + '> ' + for_a[2] + '</label>'
            if for_a[1] == '':
                choice = for_a[2]

            data += '' + \
                '<li class="opennamu_forge_list_1" style="margin-left: ' + str((int(for_a[0]) - 1) * 20) + 'px;">' + \
                    choice + \
                '</li>'
            ''

        data += '</ul>'

        return await render_template(
            name,
            '''
                <form method="post">
                    ''' + data + '''
                    <hr class="main_hr">
                    <button class="__ON_BUTTON__" ''' + state +  ''' type="submit">''' + await get_lang('save') + '''</button>
                </form>
            ''',
            '(' + await get_lang('admin_group') + ')',
            [['auth/list', await get_lang('return')]]
        )
