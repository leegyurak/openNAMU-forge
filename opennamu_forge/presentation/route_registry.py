from __future__ import annotations

import itertools
import os
from typing import Any

import flask

from opennamu_forge.presentation.gopennamu_gateway import python_to_golang
from opennamu_forge.presentation.routes import (
    api_bbs_w,
    api_bbs_w_comment_exter,
    api_bbs_w_comment_one_exter,
    api_bbs_w_set,
    api_func_auth_exter,
    api_func_ip,
    api_func_ip_menu,
    api_func_language_exter,
    api_image_view,
    api_list_acl,
    api_list_recent_edit_request,
    api_list_recent_edit_request_exter,
    api_setting_exter,
    api_skin_info,
    api_topic,
    api_version,
    api_w_raw,
    api_w_render_exter,
    bbs_delete,
    bbs_make,
    bbs_w,
    bbs_w_comment_tool,
    bbs_w_delete,
    bbs_w_edit,
    bbs_w_pinned,
    bbs_w_post,
    bbs_w_set,
    bbs_w_tool,
    edit_backlink_reset,
    edit_delete,
    edit_delete_file,
    edit_delete_multiple,
    edit_move,
    edit_move_all,
    edit_request,
    edit_revert,
    edit_upload,
    filter_all,
    filter_all_add,
    filter_all_delete,
    give_admin_groups,
    give_auth,
    give_delete_admin_group,
    give_user_ban,
    give_user_fix,
    list_acl,
    list_admin,
    list_admin_auth_use,
    list_admin_group,
    list_image_file,
    list_no_link,
    list_please,
    list_title_index,
    list_user,
    list_user_check,
    list_user_check_delete,
    list_user_check_submit,
    login_find,
    login_find_email,
    login_find_email_check,
    login_find_key,
    login_login,
    login_login_2fa,
    login_logout,
    login_register,
    login_register_email,
    login_register_email_check,
    login_register_submit,
    main_setting,
    main_setting_404_page,
    main_setting_email_test,
    main_setting_external,
    main_setting_head,
    main_setting_main,
    main_setting_main_logo,
    main_setting_phrase,
    main_setting_robot,
    main_setting_sitemap,
    main_setting_sitemap_set,
    main_setting_skin_set,
    main_setting_top_menu,
    main_sys_restart,
    main_sys_shutdown,
    main_tool_admin,
    main_tool_redirect,
    main_view,
    main_view_file,
    main_view_image,
    recent_app_submit,
    recent_change,
    recent_edit_request,
    recent_history_add,
    recent_history_delete,
    recent_history_hidden,
    recent_history_reset,
    recent_history_send,
    recent_history_tool,
    recent_record_reset,
    recent_record_topic,
    topic,
    topic_comment_blind,
    topic_comment_delete,
    topic_comment_notice,
    topic_comment_tool,
    topic_tool,
    topic_tool_acl,
    topic_tool_change,
    topic_tool_delete,
    topic_tool_setting,
    user_alarm,
    user_alarm_delete,
    user_challenge,
    user_count,
    user_edit_filter,
    user_setting,
    user_setting_email,
    user_setting_email_check,
    user_setting_email_delete,
    user_setting_head,
    user_setting_head_reset,
    user_setting_key,
    user_setting_key_delete,
    user_setting_pw,
    user_setting_skin_set,
    user_setting_skin_set_main,
    user_setting_top_menu,
    user_setting_user_name,
    view_diff,
    view_raw,
    view_set,
    view_w,
    view_xref,
    vote_add,
    vote_close,
    vote_end,
    vote_list,
    vote_select,
)
from opennamu_forge.presentation.theme import build_theme_css

_golang_view_seq = itertools.count()

def golang_view():
    idx = next(_golang_view_seq)

    async def _view(*args, **kwargs):
        return await python_to_golang("same")

    _view.__name__ = f"_golang_view_{idx}"
    return _view

def register_routes(app: Any, *, version_list: dict[str, str], golang_process: Any) -> None:
    # Route registration

    # Func
    # Func-inter_wiki
    app.route('/filter/inter_wiki', defaults = { 'tool' : 'inter_wiki' })(filter_all)
    app.route('/filter/inter_wiki/add', methods = ['POST', 'GET'], defaults = { 'tool' : 'inter_wiki' })(filter_all_add)
    app.route('/filter/inter_wiki/add/<everything:name>', methods = ['POST', 'GET'], defaults = { 'tool' : 'inter_wiki' })(filter_all_add)
    app.route('/filter/inter_wiki/del/<everything:name>', defaults = { 'tool' : 'inter_wiki' })(filter_all_delete)

    app.route('/filter/outer_link', defaults = { 'tool' : 'outer_link' })(filter_all)
    app.route('/filter/outer_link/add', methods = ['POST', 'GET'], defaults = { 'tool' : 'outer_link' })(filter_all_add)
    app.route('/filter/outer_link/add/<everything:name>', methods = ['POST', 'GET'], defaults = { 'tool' : 'outer_link' })(filter_all_add)
    app.route('/filter/outer_link/del/<everything:name>', defaults = { 'tool' : 'outer_link' })(filter_all_delete)

    app.route('/filter/document', defaults = { 'tool' : 'document' })(filter_all)
    app.route('/filter/document/add', methods = ['POST', 'GET'], defaults = { 'tool' : 'document' })(filter_all_add)
    app.route('/filter/document/add/<everything:name>', methods = ['POST', 'GET'], defaults = { 'tool' : 'document' })(filter_all_add)
    app.route('/filter/document/del/<everything:name>', defaults = { 'tool' : 'document' })(filter_all_delete)

    app.route('/filter/edit_top', defaults = { 'tool' : 'edit_top' })(filter_all)
    app.route('/filter/edit_top/add', methods = ['POST', 'GET'], defaults = { 'tool' : 'edit_top' })(filter_all_add)
    app.route('/filter/edit_top/add/<everything:name>', methods = ['POST', 'GET'], defaults = { 'tool' : 'edit_top' })(filter_all_add)
    app.route('/filter/edit_top/del/<everything:name>', defaults = { 'tool' : 'edit_top' })(filter_all_delete)

    app.route('/filter/image_license', defaults = { 'tool' : 'image_license' })(filter_all)
    app.route('/filter/image_license/add', methods = ['POST', 'GET'], defaults = { 'tool' : 'image_license' })(filter_all_add)
    app.route('/filter/image_license/del/<everything:name>', defaults = { 'tool' : 'image_license' })(filter_all_delete)

    app.route('/filter/template', defaults = { 'tool' : 'template' })(filter_all)
    app.route('/filter/template/add', methods = ['POST', 'GET'], defaults = { 'tool' : 'template' })(filter_all_add)
    app.route('/filter/template/add/<everything:name>', methods = ['POST', 'GET'], defaults = { 'tool' : 'template' })(filter_all_add)
    app.route('/filter/template/del/<everything:name>', defaults = { 'tool' : 'template' })(filter_all_delete)

    app.route('/filter/edit_filter', defaults = { 'tool' : 'edit_filter' })(filter_all)
    app.route('/filter/edit_filter/add', methods = ['POST', 'GET'], defaults = { 'tool' : 'edit_filter' })(filter_all_add)
    app.route('/filter/edit_filter/add/<everything:name>', methods = ['POST', 'GET'], defaults = { 'tool' : 'edit_filter' })(filter_all_add)
    app.route('/filter/edit_filter/del/<everything:name>', defaults = { 'tool' : 'edit_filter' })(filter_all_delete)

    app.route('/filter/email_filter', defaults = { 'tool' : 'email_filter' })(filter_all)
    app.route('/filter/email_filter/add', methods = ['POST', 'GET'], defaults = { 'tool' : 'email_filter' })(filter_all_add)
    app.route('/filter/email_filter/del/<everything:name>', defaults = { 'tool' : 'email_filter' })(filter_all_delete)

    app.route('/filter/file_filter', defaults = { 'tool' : 'file_filter' })(filter_all)
    app.route('/filter/file_filter/add', methods = ['POST', 'GET'], defaults = { 'tool' : 'file_filter' })(filter_all_add)
    app.route('/filter/file_filter/del/<everything:name>', defaults = { 'tool' : 'file_filter' })(filter_all_delete)

    app.route('/filter/name_filter', defaults = { 'tool' : 'name_filter' })(filter_all)
    app.route('/filter/name_filter/add', methods = ['POST', 'GET'], defaults = { 'tool' : 'name_filter' })(filter_all_add)
    app.route('/filter/name_filter/del/<everything:name>', defaults = { 'tool' : 'name_filter' })(filter_all_delete)

    app.route('/filter/extension_filter', defaults = { 'tool' : 'extension_filter' })(filter_all)
    app.route('/filter/extension_filter/add', methods = ['POST', 'GET'], defaults = { 'tool' : 'extension_filter' })(filter_all_add)
    app.route('/filter/extension_filter/del/<everything:name>', defaults = { 'tool' : 'extension_filter' })(filter_all_delete)

    # Func-list
    app.route('/list/document/old')(golang_view())
    app.route('/list/document/old/<int:num>')(golang_view())

    app.route('/list/document/new')(golang_view())
    app.route('/list/document/new/<int:num>')(golang_view())

    app.route('/list/document/no_link')(list_no_link)
    app.route('/list/document/no_link/<int:num>')(list_no_link)

    app.route('/list/document/acl')(list_acl)
    app.route('/list/document/acl/<int:arg_num>')(list_acl)

    app.route('/list/document/need')(list_please)
    app.route('/list/document/need/<int:arg_num>')(list_please)

    app.route('/list/document/all')(list_title_index)
    app.route('/list/document/all/<int:num>')(list_title_index)

    app.route('/list/document/long')(golang_view())
    app.route('/list/document/long/<int:arg_num>')(golang_view())

    app.route('/list/document/short')(golang_view())
    app.route('/list/document/short/<int:arg_num>')(golang_view())

    app.route('/list/file')(list_image_file)
    app.route('/list/file/<int:arg_num>')(list_image_file)
    app.route('/list/image', defaults = { 'do_type' : 1 })(list_image_file)
    app.route('/list/image/<int:arg_num>', defaults = { 'do_type' : 1 })(list_image_file)

    app.route('/list/admin')(list_admin)

    app.route('/list/admin/auth_use', methods = ['POST', 'GET'])(list_admin_auth_use)
    app.route('/list/admin/auth_use_page/<int:arg_num>/<everything:arg_search>', methods = ['POST', 'GET'])(list_admin_auth_use)

    app.route('/list/user')(list_user)
    app.route('/list/user/<int:arg_num>')(list_user)

    app.route('/list/user/check_submit/<name>')(list_user_check_submit)
    app.route('/list/user/check/<name>')(list_user_check)
    app.route('/list/user/check/<name>/<do_type>')(list_user_check)
    app.route('/list/user/check/<name>/<do_type>/<int:arg_num>')(list_user_check)
    app.route('/list/user/check/<name>/<do_type>/<int:arg_num>/<plus_name>')(list_user_check)
    app.route('/list/user/check/delete/<name>/<ip>/<time>/<do_type>', methods = ['POST', 'GET'])(list_user_check_delete)

    # Func-auth
    app.route('/auth/give', methods = ['POST', 'GET'])(give_auth)
    app.route('/auth/give_total', methods = ['POST', 'GET'])(give_auth)
    app.route('/auth/give/<user_name>', methods = ['POST', 'GET'])(give_auth)

    app.route('/auth/ban', methods = ['POST', 'GET'])(give_user_ban)
    app.route('/auth/ban/multiple', methods = ['POST', 'GET'], defaults = { 'ban_type' : 'multiple' })(give_user_ban)
    app.route('/auth/ban/<everything:name>', methods = ['POST', 'GET'])(give_user_ban)
    app.route('/auth/ban_cidr/<everything:name>', methods = ['POST', 'GET'], defaults = { 'ban_type' : 'cidr' })(give_user_ban)
    app.route('/auth/ban_regex/<everything:name>', methods = ['POST', 'GET'], defaults = { 'ban_type' : 'regex' })(give_user_ban)

    # /auth/list
    # /auth/list/add/<name>
    # /auth/list/delete/<name>
    app.route('/auth/list')(list_admin_group)
    app.route('/auth/list/add/<name>', methods = ['POST', 'GET'])(give_admin_groups)
    app.route('/auth/list/delete/<name>', methods = ['POST', 'GET'])(give_delete_admin_group)

    app.route('/auth/give/fix/<user_name>', methods = ['POST', 'GET'])(give_user_fix)

    app.route('/app_submit', methods = ['POST', 'GET'])(recent_app_submit)

    # /auth/history
    app.route('/recent_block')(golang_view())
    app.route('/recent_block/all')(golang_view())
    app.route('/recent_block/all/<int:num>')(golang_view())
    app.route('/recent_block/all/<int:num>/<everything:why>')(golang_view())
    app.route('/recent_block/user/<user_name>')(golang_view())
    app.route('/recent_block/user/<user_name>/<int:num>')(golang_view())
    app.route('/recent_block/admin/<user_name>')(golang_view())
    app.route('/recent_block/admin/<user_name>/<int:num>')(golang_view())
    app.route('/recent_block/regex')(golang_view())
    app.route('/recent_block/regex/<int:num>')(golang_view())
    app.route('/recent_block/cidr')(golang_view())
    app.route('/recent_block/cidr/<int:num>')(golang_view())
    app.route('/recent_block/private')(golang_view())
    app.route('/recent_block/private/<int:num>')(golang_view())
    app.route('/recent_block/ongoing')(golang_view())
    app.route('/recent_block/ongoing/<int:num>')(golang_view())

    app.route('/recent_change')(golang_view())
    app.route('/recent_changes')(golang_view())
    app.route('/recent_change/<int:num>/<set_type>')(golang_view())

    app.route('/recent_discuss')(golang_view())
    app.route('/recent_discuss/<int:num>/<tool>')(golang_view())

    # Func-history
    app.route('/recent_edit_request')(recent_edit_request)

    app.route('/record/<name>', defaults = { 'tool' : 'record' })(recent_change)
    app.route('/record/<int:num>/<set_type>/<name>', defaults = { 'tool' : 'record' })(recent_change)

    app.route('/record/reset/<name>', methods = ['POST', 'GET'])(recent_record_reset)
    app.route('/record/topic/<name>')(recent_record_topic)

    app.route('/record/bbs/<name>', defaults = { 'tool' : 'record' })(bbs_w)
    app.route('/record/bbs_comment/<name>', defaults = { 'tool' : 'comment_record' })(bbs_w)

    app.route('/history/<everything:doc_name>', methods = ['POST', 'GET'])(golang_view())
    app.route('/history_page/<int:num>/<set_type>/<everything:doc_name>', methods = ['POST', 'GET'])(golang_view())

    app.route('/history_tool/<int(signed = True):rev>/<everything:name>')(recent_history_tool)
    app.route('/history_delete/<int(signed = True):rev>/<everything:name>', methods = ['POST', 'GET'])(recent_history_delete)
    app.route('/history_hidden/<int(signed = True):rev>/<everything:name>')(recent_history_hidden)
    app.route('/history_send/<int(signed = True):rev>/<everything:name>', methods = ['POST', 'GET'])(recent_history_send)
    app.route('/history_reset/<everything:name>', methods = ['POST', 'GET'])(recent_history_reset)
    app.route('/history_add/<everything:name>', methods = ['POST', 'GET'])(recent_history_add)

    # Func-view
    app.route('/xref/<everything:name>')(view_xref)
    app.route('/xref_page/<int:num>/<everything:name>')(view_xref)
    app.route('/xref_this/<everything:name>', defaults = { 'xref_type' : 2 })(view_xref)
    app.route('/xref_this_page/<int:num>/<everything:name>', defaults = { 'xref_type' : 2 })(view_xref)

    app.route('/doc_watch_list/<int:num>/<everything:name>')(golang_view())
    app.route('/doc_star_doc/<int:num>/<everything:name>')(golang_view())

    app.route('/raw/<everything:name>')(golang_view())
    app.route('/raw_acl/<everything:name>')(golang_view())
    app.route('/raw_rev/<int(signed = True):rev>/<everything:name>')(golang_view())

    app.route('/diff/<int(signed = True):num_a>/<int(signed = True):num_b>/<everything:name>')(view_diff)

    app.route('/down/<everything:name>')(golang_view())

    app.route('/acl_multiple', defaults = { 'multiple' : True }, methods = ['POST', 'GET'])(view_set)
    app.route('/acl/<everything:name>', methods = ['POST', 'GET'])(view_set)

    app.route('/render/<int:doc_rev>/<everything:name>')(view_w)

    app.route('/w_from/<everything:name>', defaults = { 'do_type' : 'from' })(view_w)
    app.route('/w/<everything:name>')(view_w)

    app.route('/random')(golang_view())
    app.route('/list/random')(golang_view())

    # Func-edit
    app.route('/edit/<everything:name>', methods = ['POST', 'GET'])(golang_view())
    app.route('/edit_from/<everything:name>', methods = ['POST', 'GET'])(golang_view())

    app.route('/edit_request/<everything:name>', methods = ['POST', 'GET'])(edit_request)
    app.route('/edit_request_from/<everything:name>', defaults = { 'do_type' : 'from' }, methods = ['POST', 'GET'])(edit_request)

    # app.route('/edit_request_rev/<int:rev>/<everything:name>', methods = ['POST', 'GET'])(edit_request)

    app.route('/upload', methods = ['POST', 'GET'])(edit_upload)

    # 개편 예정
    app.route('/xref_reset/<everything:name>')(edit_backlink_reset)

    app.route('/delete/<everything:name>', methods = ['POST', 'GET'])(edit_delete)
    app.route('/delete_file/<everything:name>', methods = ['POST', 'GET'])(edit_delete_file)
    app.route('/delete_multiple', methods = ['POST', 'GET'])(edit_delete_multiple)

    app.route('/revert/<int:num>/<everything:name>', methods = ['POST', 'GET'])(edit_revert)

    app.route('/move/<everything:name>', methods = ['POST', 'GET'])(edit_move)
    app.route('/move_all')(edit_move_all)

    # Func-topic
    app.route('/topic/<everything:name>')(golang_view())
    app.route('/topic_page/<int:page>/<everything:name>')(golang_view())
    app.route('/topic_close/<int:page>/<everything:name>')(golang_view())
    app.route('/topic_agree/<int:page>/<everything:name>')(golang_view())

    app.route('/thread/<int:topic_num>', methods = ['POST', 'GET'])(topic)
    app.route('/thread/0/<everything:doc_name>', defaults = { 'topic_num' : '0' }, methods = ['POST', 'GET'])(topic)

    app.route('/thread/<int:topic_num>/tool')(topic_tool)
    app.route('/thread/<int:topic_num>/setting', methods = ['POST', 'GET'])(topic_tool_setting)
    app.route('/thread/<int:topic_num>/acl', methods = ['POST', 'GET'])(topic_tool_acl)
    app.route('/thread/<int:topic_num>/delete', methods = ['POST', 'GET'])(topic_tool_delete)
    app.route('/thread/<int:topic_num>/change', methods = ['POST', 'GET'])(topic_tool_change)

    app.route('/thread/<int:topic_num>/comment/<int:num>/tool')(topic_comment_tool)
    app.route('/thread/<int:topic_num>/comment/<int:num>/notice')(topic_comment_notice)
    app.route('/thread/<int:topic_num>/comment/<int:num>/blind')(topic_comment_blind)
    app.route('/thread/<int:topic_num>/comment/<int:num>/raw')(view_raw)
    app.route('/thread/<int:topic_num>/comment/<int:num>/delete', methods = ['POST', 'GET'])(topic_comment_delete)

    # Func-user
    app.route('/change', methods = ['POST', 'GET'])(user_setting)
    app.route('/change/key')(user_setting_key)
    app.route('/change/key/delete')(user_setting_key_delete)
    app.route('/change/pw', methods = ['POST', 'GET'])(user_setting_pw)
    app.route('/change/head', methods = ['GET', 'POST'], defaults = { 'skin_name' : '' })(user_setting_head)
    app.route('/change/head/<skin_name>', methods = ['GET', 'POST'])(user_setting_head)
    app.route('/change/head_reset', methods = ['GET', 'POST'])(user_setting_head_reset)
    app.route('/change/skin_set')(user_setting_skin_set)
    app.route('/change/top_menu', methods = ['GET', 'POST'])(user_setting_top_menu)
    app.route('/change/user_name', methods = ['GET', 'POST'])(user_setting_user_name)
    app.route('/change/user_name/<user_name>', methods = ['GET', 'POST'])(user_setting_user_name)
    app.route('/change/skin_set/main', methods = ['POST', 'GET'])(user_setting_skin_set_main)

    app.route('/user')(golang_view())
    app.route('/user/<name>')(golang_view())

    app.route('/challenge', methods = ['GET', 'POST'])(user_challenge)

    app.route('/edit_filter/<name>', methods = ['GET', 'POST'])(user_edit_filter)

    app.route('/count')(user_count)
    app.route('/count/<name>')(user_count)

    app.route('/alarm')(user_alarm)
    app.route('/alarm/delete')(user_alarm_delete)
    app.route('/alarm/delete/<int:id>')(user_alarm_delete)

    app.route('/watch_list')(golang_view())
    app.route('/watch_list/<everything:name>', methods = ['POST', 'GET'])(golang_view())
    app.route('/watch_list_from/<everything:name>', methods = ['POST', 'GET'])(golang_view())

    app.route('/star_doc')(golang_view())
    app.route('/star_doc/<everything:name>', methods = ['POST', 'GET'])(golang_view())
    app.route('/star_doc_from/<everything:name>', methods = ['POST', 'GET'])(golang_view())

    # 개편 보류중 S
    app.route('/change/email', methods = ['POST', 'GET'])(user_setting_email)
    app.route('/change/email/delete')(user_setting_email_delete)
    app.route('/change/email/check', methods = ['POST', 'GET'])(user_setting_email_check)
    # 개편 보류중 E

    # Func-login
    # 개편 예정

    # login -> login/2fa -> login/2fa/email with login_id
    # register -> register/email -> regiter/email/check with reg_id
    # pass_find -> pass_find/email with find_id

    app.route('/login', methods = ['POST', 'GET'])(login_login)
    app.route('/login/2fa', methods = ['POST', 'GET'])(login_login_2fa)
    app.route('/register', methods = ['POST', 'GET'])(login_register)
    app.route('/register/email', methods = ['POST', 'GET'])(login_register_email)
    app.route('/register/email/check', methods = ['POST', 'GET'])(login_register_email_check)
    app.route('/register/submit', methods = ['POST', 'GET'])(login_register_submit)

    app.route('/login/find')(login_find)
    app.route('/login/find/key', methods = ['POST', 'GET'])(login_find_key)
    app.route('/login/find/email', methods = ['POST', 'GET'], defaults = { 'tool' : 'pass_find' })(login_find_email)
    app.route('/login/find/email/check', methods = ['POST', 'GET'], defaults = { 'tool' : 'check_key' })(login_find_email_check)
    app.route('/logout')(login_logout)

    # Func-vote
    app.route('/vote/<int:num>', methods = ['POST', 'GET'])(vote_select)
    app.route('/vote/end/<int:num>')(vote_end)
    app.route('/vote/close/<int:num>')(vote_close)
    app.route('/vote', defaults = { 'list_type' : 'normal' })(vote_list)
    app.route('/vote/list', defaults = { 'list_type' : 'normal' })(vote_list)
    app.route('/vote/list/<int:num>', defaults = { 'list_type' : 'normal' })(vote_list)
    app.route('/vote/list/close', defaults = { 'list_type' : 'close' })(vote_list)
    app.route('/vote/list/close/<int:num>', defaults = { 'list_type' : 'close' })(vote_list)
    app.route('/vote/add', methods = ['POST', 'GET'])(vote_add)

    # Func-bbs
    app.route('/bbs/main')(golang_view())
    app.route('/bbs/make', methods = ['POST', 'GET'])(bbs_make)
    app.route('/bbs/in/<int:bbs_num>')(golang_view())
    app.route('/bbs/in/<int:bbs_num>/<int:page>')(golang_view())
    # app.route('/bbs/blind/<int:bbs_num>', methods = ['POST', 'GET'])(bbs_hide)
    app.route('/bbs/delete/<int:bbs_num>', methods = ['POST', 'GET'])(bbs_delete)
    app.route('/bbs/set/<int:bbs_num>', methods = ['POST', 'GET'])(bbs_w_set)
    app.route('/bbs/edit/<int:bbs_num>', methods = ['POST', 'GET'])(bbs_w_edit)
    app.route('/bbs/w/<int:bbs_num>/<int:post_num>', methods = ['POST'])(bbs_w_post)
    app.route('/bbs/w/<int:bbs_num>/<int:post_num>', methods = ['GET'])(golang_view())
    # app.route('/bbs/blind/<int:bbs_num>/<int:post_num>', methods = ['POST', 'GET'])(bbs_w_hide)
    app.route('/bbs/pinned/<int:bbs_num>/<int:post_num>', methods = ['POST', 'GET'])(bbs_w_pinned)
    app.route('/bbs/delete/<int:bbs_num>/<int:post_num>', methods = ['POST', 'GET'])(bbs_w_delete)
    app.route('/bbs/raw/<int:bbs_num>/<int:post_num>')(view_raw)
    app.route('/bbs/tool/<int:bbs_num>/<int:post_num>')(bbs_w_tool)
    app.route('/bbs/edit/<int:bbs_num>/<int:post_num>', methods = ['POST', 'GET'])(bbs_w_edit)
    app.route('/bbs/tool/<int:bbs_num>/<int:post_num>/<comment_num>')(bbs_w_comment_tool)
    app.route('/bbs/raw/<int:bbs_num>/<int:post_num>/<comment_num>')(view_raw)
    app.route('/bbs/edit/<int:bbs_num>/<int:post_num>/<comment_num>', methods = ['POST', 'GET'])(bbs_w_edit)
    app.route('/bbs/delete/<int:bbs_num>/<int:post_num>/<comment_num>', methods = ['POST', 'GET'])(bbs_w_delete)

    # Func-api
    ## v1 API
    app.route('/api/render', methods = ['POST'])(api_w_render_exter)
    app.route('/api/render/<tool>', methods = ['POST'])(api_w_render_exter)

    app.route('/api/raw_exist/<everything:name>', defaults = { 'exist_check' : 'on' })(api_w_raw)
    app.route('/api/raw_rev/<int(signed = True):rev>/<everything:name>')(api_w_raw)
    app.route('/api/raw/<everything:name>')(api_w_raw)

    app.route('/api/xref/<int:page>/<everything:name>')(golang_view())
    app.route('/api/xref_this/<int:page>/<everything:name>')(golang_view())

    app.route('/api/random')(golang_view())

    app.route('/api/bbs/w/<sub_code>')(api_bbs_w)
    app.route('/api/bbs/w/comment/<sub_code>')(api_bbs_w_comment_exter)
    app.route('/api/bbs/w/comment_one/<sub_code>')(api_bbs_w_comment_one_exter)

    app.route('/api/version', defaults = { 'version_list' : version_list })(api_version)
    app.route('/api/skin_info')(api_skin_info)
    app.route('/api/skin_info/<name>')(api_skin_info)
    app.route('/api/user_info/<user_name>')(golang_view())

    app.route('/api/thread/<int:topic_num>/<int:s_num>/<int:e_num>')(api_topic)
    app.route('/api/thread/<int:topic_num>/<tool>')(api_topic)
    app.route('/api/thread/<int:topic_num>')(api_topic)

    app.route('/api/search/<everything:name>')(golang_view())
    app.route('/api/search_page/<int:num>/<everything:name>')(golang_view())
    app.route('/api/search_data/<everything:name>', defaults = { 'search_type' : 'data' })(golang_view())
    app.route('/api/search_data_page/<int:num>/<everything:name>', defaults = { 'search_type' : 'data' })(golang_view())

    app.route('/api/recent_change')(golang_view())
    app.route('/api/recent_changes')(golang_view())
    app.route('/api/recent_change/<int:limit>')(golang_view())
    app.route('/api/recent_change/<int:limit>/<set_type>/<int:num>')(golang_view())

    app.route('/api/recent_edit_request')(api_list_recent_edit_request_exter)
    app.route('/api/recent_edit_request/<int:limit>/<set_type>/<int:num>')(api_list_recent_edit_request_exter)

    app.route('/api/recent_discuss/<set_type>/<int:limit>')(golang_view())
    app.route('/api/recent_discuss/<int:limit>')(golang_view())
    app.route('/api/recent_discuss')(golang_view())

    app.route('/api/lang', methods = ['POST'])(api_func_language_exter)
    app.route('/api/lang/<data>')(api_func_language_exter)
    app.route('/api/sha224/<everything:data>')(golang_view())
    app.route('/api/ip/<everything:data>')(api_func_ip)

    app.route('/api/image/<everything:name>')(api_image_view)

    ## v2 API
    app.route('/api/v2/recent_edit_request/<set_type>/<int:num>', defaults = { 'limit' : 50 })(api_list_recent_edit_request)
    app.route('/api/v2/recent_change/<set_type>/<int:num>')(golang_view())
    app.route('/api/v2/recent_discuss/<set_type>/<int:num>')(golang_view())
    app.route('/api/v2/recent_block/<set_type>/<int:num>')(golang_view())
    app.route('/api/v2/recent_block/<set_type>/<int:num>/<everything:why>')(golang_view())
    app.route('/api/v2/recent_block_user/<set_type>/<int:num>/<user_name>')(golang_view())
    app.route('/api/v2/recent_block_user/<set_type>/<int:num>/<user_name>/<everything:why>')(golang_view())
    app.route('/api/v2/list/document/old/<int:num>')(golang_view())
    app.route('/api/v2/list/document/new/<int:num>')(golang_view())
    app.route('/api/v2/list/document/<int:num>')(golang_view())
    app.route('/api/v2/list/auth')(golang_view())
    app.route('/api/v2/list/markup')(golang_view())
    app.route('/api/v2/list/acl/<data_type>')(api_list_acl)
    app.route('/api/v2/history/<int:num>/<set_type>/<everything:doc_name>')(golang_view())

    app.route('/api/v2/topic/<int:num>/<set_type>/<everything:name>')(golang_view())

    app.route('/api/v2/bbs')(golang_view())
    app.route('/api/v2/bbs/main')(golang_view())
    app.route('/api/v2/bbs/set/<int:bbs_num>/<name>', methods = ['GET', 'PUT'])(api_bbs_w_set)
    app.route('/api/v2/bbs/in/<int:bbs_num>/<int:page>')(golang_view())

    app.route('/api/v2/bbs/w/<sub_code>', defaults = { 'include_envelope' : True })(api_bbs_w)
    app.route('/api/v2/bbs/w/tabom/<sub_code>', methods = ['GET', 'POST'])(golang_view())
    app.route('/api/v2/bbs/w/comment/<sub_code>/<tool>', defaults = { 'include_envelope' : True })(api_bbs_w_comment_exter)
    app.route('/api/v2/bbs/w/comment_one/<sub_code>/<tool>')(api_bbs_w_comment_one_exter)

    app.route('/api/v2/bbs/w/page_view/<set_id>/<set_code>')(golang_view())
    app.route('/api/v2/bbs/w/page_view_post/<set_id>/<set_code>')(golang_view())

    app.route('/api/v2/doc_star_doc/<int:num>/<everything:name>', defaults = { 'do_type' : 'star_doc' })(golang_view())
    app.route('/api/v2/doc_watch_list/<int:num>/<everything:name>')(golang_view())
    app.route('/api/v2/set_reset/<everything:name>')(golang_view())

    app.route('/api/v2/page_view/<everything:name>')(golang_view())
    app.route('/api/v2/page_view_post/<everything:name>')(golang_view())

    app.route('/api/v2/setting/<name>', methods = ['GET', 'PUT'])(api_setting_exter)

    app.route('/api/v2/auth')(api_func_auth_exter)
    app.route('/api/v2/auth/<user_name>')(api_func_auth_exter)
    app.route('/api/v2/auth/give', methods = ['PATCH'])(golang_view())

    app.route('/api/v2/user/rankup', methods = ['GET', 'PATCH'])(golang_view())
    app.route('/api/v2/user/setting/editor', methods = ['GET', 'POST', 'DELETE'])(golang_view())

    app.route('/api/v2/ip/<everything:data>', methods = ['GET', 'POST'])(api_func_ip)
    app.route('/api/v2/ip_menu/<everything:ip>', defaults = { 'option' : 'user' }, methods = ['GET', 'POST'])(api_func_ip_menu)
    app.route('/api/v2/user_menu/<everything:ip>')(api_func_ip_menu)
    app.route('/api/v2/lang', methods = ['POST'])(api_func_language_exter)

    # Func-main
    # 여기도 전반적인 조정 시행 예정
    app.route('/other')(golang_view())
    app.route('/manager', methods = ['POST', 'GET'])(main_tool_admin)
    app.route('/manager/<int:num>', methods = ['POST', 'GET'])(main_tool_redirect)
    app.route('/manager/<int:num>/<everything:add_2>', methods = ['POST', 'GET'])(main_tool_redirect)

    app.route('/search/<everything:name>', methods = ['GET'])(golang_view())
    app.route('/goto/<everything:name>', methods = ['GET'])(golang_view())
    app.route('/search_page/<int:num>/<everything:name>', methods = ['GET'])(golang_view())
    app.route('/search_data/<everything:name>', methods = ['GET'])(golang_view())
    app.route('/search_data_page/<int:num>/<everything:name>', methods = ['GET'])(golang_view())

    app.route('/goto', methods = ['POST'])(golang_view())
    app.route('/goto/<everything:name>', methods = ['POST'])(golang_view())
    app.route('/search', methods = ['POST'])(golang_view())
    app.route('/search/<everything:name>', methods = ['POST'])(golang_view())
    app.route('/search_page/<int:num>/<everything:name>', methods = ['POST'])(golang_view())
    app.route('/search_data/<everything:name>', methods = ['POST'])(golang_view())
    app.route('/search_data_page/<int:num>/<everything:name>', methods = ['POST'])(golang_view())

    app.route('/setting')(main_setting)
    app.route('/setting/main', methods = ['POST', 'GET'])(main_setting_main)
    app.route('/setting/main/logo', methods = ['POST', 'GET'])(main_setting_main_logo)
    app.route('/setting/top_menu', methods = ['POST', 'GET'])(main_setting_top_menu)
    app.route('/setting/phrase', methods = ['POST', 'GET'])(main_setting_phrase)
    app.route('/setting/head', defaults = { 'num' : 3 }, methods = ['POST', 'GET'])(main_setting_head)
    app.route('/setting/head/<skin_name>', defaults = { 'num' : 3 }, methods = ['POST', 'GET'])(main_setting_head)
    app.route('/setting/body/top', defaults = { 'num' : 4 }, methods = ['POST', 'GET'])(main_setting_head)
    app.route('/setting_preview/body/top', defaults = { 'num' : 4, 'set_preview' : 1 }, methods = ['POST'])(main_setting_head)
    app.route('/setting/body/bottom', defaults = { 'num' : 7 }, methods = ['POST', 'GET'])(main_setting_head)
    app.route('/setting_preview/body/bottom', defaults = { 'num' : 7, 'set_preview' : 1 }, methods = ['POST'])(main_setting_head)
    app.route('/setting/robot', methods = ['POST', 'GET'])(main_setting_robot)
    app.route('/setting/external', methods = ['POST', 'GET'])(main_setting_external)
    app.route('/setting/sitemap', methods = ['POST', 'GET'])(main_setting_sitemap)
    app.route('/setting/sitemap_set', methods = ['POST', 'GET'])(main_setting_sitemap_set)
    app.route('/setting/skin_set', methods = ['POST', 'GET'])(main_setting_skin_set)
    app.route('/setting/404_page', methods = ['POST', 'GET'])(main_setting_404_page)
    app.route('/setting/email_test', methods = ['POST', 'GET'])(main_setting_email_test)

    # views -> view
    app.route('/view/<path:name>')(main_view)
    app.route('/views/<path:name>')(main_view)
    app.route('/image/<path:name>')(main_view_image)
    # 조정 계획 중
    app.route('/<regex("[^.]+\\.(?:txt|xml|ico)"):data>')(main_view_file)

    @app.get('/forge/theme.css.cache_v1')
    def opennamu_forge_theme_css():
        return flask.Response(build_theme_css(os.getenv('NAMU_THEME_COLOR')), mimetype='text/css')

    app.route('/shutdown', methods = ['POST', 'GET'])(main_sys_shutdown)
    app.route('/restart', defaults = { 'golang_process' : golang_process }, methods = ['POST', 'GET'])(main_sys_restart)

    app.errorhandler(404)(golang_view())
