import subprocess
from pathlib import Path

import pytest

ROUTE_FILES = tuple(Path("opennamu_forge/presentation/routes").glob("*.py"))
CONVERTED_SUPPORT_FILES = (
    Path("opennamu_forge/presentation/runtime_app.py"),
    Path("opennamu_forge/presentation/rendering/renderer.py"),
    Path("opennamu_forge/presentation/rendering/namumark.py"),
    Path("opennamu_forge/presentation/shared/func.py"),
)
CONVERTED_DB_FREE_ROUTE_FILES = (
    Path("opennamu_forge/presentation/routes/api_skin_info.py"),
    Path("opennamu_forge/presentation/routes/api_version.py"),
    Path("opennamu_forge/presentation/routes/api_image_view.py"),
    Path("opennamu_forge/presentation/routes/bbs_delete.py"),
    Path("opennamu_forge/presentation/routes/bbs_w_comment_tool.py"),
    Path("opennamu_forge/presentation/routes/bbs_w.py"),
    Path("opennamu_forge/presentation/routes/bbs_w_delete.py"),
    Path("opennamu_forge/presentation/routes/bbs_w_hide.py"),
    Path("opennamu_forge/presentation/routes/bbs_w_pinned.py"),
    Path("opennamu_forge/presentation/routes/bbs_w_tool.py"),
    Path("opennamu_forge/presentation/routes/go_api_topic.py"),
    Path("opennamu_forge/presentation/routes/list_acl.py"),
    Path("opennamu_forge/presentation/routes/list_admin.py"),
    Path("opennamu_forge/presentation/routes/list_admin_auth_use.py"),
    Path("opennamu_forge/presentation/routes/list_admin_group.py"),
    Path("opennamu_forge/presentation/routes/list_no_link.py"),
    Path("opennamu_forge/presentation/routes/list_please.py"),
    Path("opennamu_forge/presentation/routes/list_title_index.py"),
    Path("opennamu_forge/presentation/routes/list_user.py"),
    Path("opennamu_forge/presentation/routes/login_logout.py"),
    Path("opennamu_forge/presentation/routes/main_setting.py"),
    Path("opennamu_forge/presentation/routes/main_tool_redirect.py"),
    Path("opennamu_forge/presentation/routes/n_bbs_w_set.py"),
    Path("opennamu_forge/presentation/routes/recent_change.py"),
    Path("opennamu_forge/presentation/routes/recent_edit_request.py"),
    Path("opennamu_forge/presentation/routes/recent_history_hidden.py"),
    Path("opennamu_forge/presentation/routes/recent_history_tool.py"),
    Path("opennamu_forge/presentation/routes/recent_record_topic.py"),
    Path("opennamu_forge/presentation/routes/topic_tool.py"),
    Path("opennamu_forge/presentation/routes/user_alarm.py"),
    Path("opennamu_forge/presentation/routes/user_alarm_delete.py"),
    Path("opennamu_forge/presentation/routes/user_challenge.py"),
    Path("opennamu_forge/presentation/routes/user_count.py"),
    Path("opennamu_forge/presentation/routes/user_edit_filter.py"),
    Path("opennamu_forge/presentation/routes/user_setting_email_check.py"),
    Path("opennamu_forge/presentation/routes/user_setting_email_delete.py"),
    Path("opennamu_forge/presentation/routes/user_setting_head.py"),
    Path("opennamu_forge/presentation/routes/user_setting_head_reset.py"),
    Path("opennamu_forge/presentation/routes/user_setting_key.py"),
    Path("opennamu_forge/presentation/routes/user_setting_key_delete.py"),
    Path("opennamu_forge/presentation/routes/vote_end.py"),
    Path("opennamu_forge/presentation/routes/vote_list.py"),
    Path("opennamu_forge/presentation/routes/vote_select.py"),
)


@pytest.mark.parametrize(
    "route_file",
    [
        "opennamu_forge/presentation/routes/main_setting_external.py",
        "opennamu_forge/presentation/routes/main_setting_head.py",
        "opennamu_forge/presentation/routes/main_setting_main.py",
        "opennamu_forge/presentation/routes/main_setting_main_logo.py",
        "opennamu_forge/presentation/routes/main_setting_phrase.py",
        "opennamu_forge/presentation/routes/main_setting_robot.py",
        "opennamu_forge/presentation/routes/main_setting_sitemap.py",
        "opennamu_forge/presentation/routes/main_setting_sitemap_set.py",
        "opennamu_forge/presentation/routes/main_setting_skin_set.py",
        "opennamu_forge/presentation/routes/main_setting_top_menu.py",
        "opennamu_forge/presentation/routes/main_view_file.py",
        "opennamu_forge/presentation/routes/list_image_file.py",
        "opennamu_forge/presentation/routes/list_no_link.py",
        "opennamu_forge/presentation/routes/list_title_index.py",
        "opennamu_forge/presentation/routes/api_version.py",
        "opennamu_forge/presentation/routes/bbs_delete.py",
        "opennamu_forge/presentation/routes/bbs_make.py",
        "opennamu_forge/presentation/routes/bbs_w_delete.py",
        "opennamu_forge/presentation/routes/bbs_w.py",
        "opennamu_forge/presentation/routes/bbs_w_hide.py",
        "opennamu_forge/presentation/routes/bbs_w_edit.py",
        "opennamu_forge/presentation/routes/bbs_w_pinned.py",
        "opennamu_forge/presentation/routes/bbs_w_post.py",
        "opennamu_forge/presentation/routes/bbs_w_tool.py",
        "opennamu_forge/presentation/routes/edit.py",
        "opennamu_forge/presentation/routes/edit_backlink_reset.py",
        "opennamu_forge/presentation/routes/edit_delete.py",
        "opennamu_forge/presentation/routes/edit_move.py",
        "opennamu_forge/presentation/routes/edit_request.py",
        "opennamu_forge/presentation/routes/edit_revert.py",
        "opennamu_forge/presentation/routes/edit_upload.py",
        "opennamu_forge/presentation/routes/filter_all.py",
        "opennamu_forge/presentation/routes/filter_all_add.py",
        "opennamu_forge/presentation/routes/filter_all_delete.py",
        "opennamu_forge/presentation/routes/give_admin_groups.py",
        "opennamu_forge/presentation/routes/give_delete_admin_group.py",
        "opennamu_forge/presentation/routes/give_user_ban.py",
        "opennamu_forge/presentation/routes/give_user_fix.py",
        "opennamu_forge/presentation/routes/go_api_topic.py",
        "opennamu_forge/presentation/routes/go_api_w_render.py",
        "opennamu_forge/presentation/routes/list_admin.py",
        "opennamu_forge/presentation/routes/list_admin_auth_use.py",
        "opennamu_forge/presentation/routes/list_admin_group.py",
        "opennamu_forge/presentation/routes/list_acl.py",
        "opennamu_forge/presentation/routes/list_user.py",
        "opennamu_forge/presentation/routes/list_user_check.py",
        "opennamu_forge/presentation/routes/list_user_check_delete.py",
        "opennamu_forge/presentation/routes/list_please.py",
        "opennamu_forge/presentation/routes/login_find_email.py",
        "opennamu_forge/presentation/routes/login_find_email_check.py",
        "opennamu_forge/presentation/routes/login_find_key.py",
        "opennamu_forge/presentation/routes/login_register_submit.py",
        "opennamu_forge/presentation/routes/login_register_email.py",
        "opennamu_forge/presentation/routes/login_login.py",
        "opennamu_forge/presentation/routes/login_login_2fa.py",
        "opennamu_forge/presentation/routes/login_login_2fa_email.py",
        "opennamu_forge/presentation/routes/main_tool_redirect.py",
        "opennamu_forge/presentation/routes/n_bbs_w_set.py",
        "opennamu_forge/presentation/routes/recent_app_submit.py",
        "opennamu_forge/presentation/routes/recent_history_delete.py",
        "opennamu_forge/presentation/routes/recent_history_hidden.py",
        "opennamu_forge/presentation/routes/recent_history_reset.py",
        "opennamu_forge/presentation/routes/recent_history_send.py",
        "opennamu_forge/presentation/routes/recent_history_tool.py",
        "opennamu_forge/presentation/routes/recent_change.py",
        "opennamu_forge/presentation/routes/recent_record_reset.py",
        "opennamu_forge/presentation/routes/recent_record_topic.py",
        "opennamu_forge/presentation/routes/topic_comment_blind.py",
        "opennamu_forge/presentation/routes/topic_comment_delete.py",
        "opennamu_forge/presentation/routes/topic_comment_notice.py",
        "opennamu_forge/presentation/routes/topic_comment_tool.py",
        "opennamu_forge/presentation/routes/topic_tool.py",
        "opennamu_forge/presentation/routes/topic.py",
        "opennamu_forge/presentation/routes/topic_tool_acl.py",
        "opennamu_forge/presentation/routes/topic_tool_change.py",
        "opennamu_forge/presentation/routes/topic_tool_delete.py",
        "opennamu_forge/presentation/routes/topic_tool_setting.py",
        "opennamu_forge/presentation/routes/user_challenge.py",
        "opennamu_forge/presentation/routes/user_count.py",
        "opennamu_forge/presentation/routes/user_alarm.py",
        "opennamu_forge/presentation/routes/user_alarm_delete.py",
        "opennamu_forge/presentation/routes/user_edit_filter.py",
        "opennamu_forge/presentation/routes/user_setting.py",
        "opennamu_forge/presentation/routes/user_setting_email.py",
        "opennamu_forge/presentation/routes/user_setting_email_check.py",
        "opennamu_forge/presentation/routes/user_setting_email_delete.py",
        "opennamu_forge/presentation/routes/user_setting_head.py",
        "opennamu_forge/presentation/routes/user_setting_head_reset.py",
        "opennamu_forge/presentation/routes/user_setting_key.py",
        "opennamu_forge/presentation/routes/user_setting_key_delete.py",
        "opennamu_forge/presentation/routes/user_setting_pw.py",
        "opennamu_forge/presentation/routes/user_setting_skin_set_main.py",
        "opennamu_forge/presentation/routes/user_watch_list_name.py",
        "opennamu_forge/presentation/routes/user_setting_top_menu.py",
        "opennamu_forge/presentation/routes/user_setting_user_name.py",
        "opennamu_forge/presentation/routes/user_setting_skin_set.py",
        "opennamu_forge/presentation/routes/vote_add.py",
        "opennamu_forge/presentation/routes/vote_close.py",
        "opennamu_forge/presentation/routes/vote_end.py",
        "opennamu_forge/presentation/routes/vote_list.py",
        "opennamu_forge/presentation/routes/vote_select.py",
        "opennamu_forge/presentation/routes/view_diff.py",
        "opennamu_forge/presentation/routes/view_raw.py",
        "opennamu_forge/presentation/routes/view_set.py",
        "opennamu_forge/presentation/routes/view_w.py",
        "opennamu_forge/presentation/routes/view_xref.py",
    ],
)
def test_설정_route는_raw_sql을_직접_사용하지_않는다(route_file):
    source = Path(route_file).read_text(encoding="utf-8")

    assert "curs.execute" not in source
    assert "curs.executemany" not in source
    assert "db_change(" not in source


@pytest.mark.parametrize("route_file", ROUTE_FILES, ids=str)
def test_route는_other_설정_테이블을_sql로_직접_조회하지_않는다(route_file):
    source = route_file.read_text(encoding="utf-8")

    assert "select data from other" not in source
    assert "from other where name" not in source


@pytest.mark.parametrize("support_file", CONVERTED_SUPPORT_FILES, ids=str)
def test_runtime과_shared_helper는_raw_sql을_직접_사용하지_않는다(support_file):
    source = support_file.read_text(encoding="utf-8")

    assert "curs.execute" not in source
    assert "curs.executemany" not in source
    assert "db_change(" not in source
    assert "select data from other" not in source
    assert "from other where name" not in source


@pytest.mark.parametrize("route_file", CONVERTED_DB_FREE_ROUTE_FILES, ids=str)
def test_전환된_route는_db_connection을_직접_열지_않는다(route_file):
    source = route_file.read_text(encoding="utf-8")

    assert "with get_db_connect(" not in source
    assert "get_db_connect," not in source


@pytest.mark.requires_ripgrep
def test_project_code는_legacy_db_connection을_재도입하지_않는다():
    result = subprocess.run(
        ["rg", "-n", "get_db_connect|shared/db_connection|db_connection\\.py", "opennamu_forge"],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 1, result.stdout


def test_rendering_module은_shared_legacy_경로로_두지_않는다():
    assert not Path("opennamu_forge/presentation/shared/func_render.py").exists()
    assert not Path("opennamu_forge/presentation/shared/func_render_namumark.py").exists()
    assert Path("opennamu_forge/presentation/rendering/renderer.py").exists()
    assert Path("opennamu_forge/presentation/rendering/namumark.py").exists()


@pytest.mark.requires_ripgrep
def test_route와_runtime은_repository_factory를_shared_func에서_import하지_않는다():
    result = subprocess.run(
        [
            "rg",
            "-n",
            "-U",
            (
                "from opennamu_forge\\.presentation\\.shared\\.func import "
                "\\([^)]*get_(admin|backlink|bbs|document_meta|history|html_filter|other_setting|recent_block|"
                "topic|user_agent|user_notice|user_setting|vote|wiki_document)_repository"
                "|from opennamu_forge\\.presentation\\.shared\\.func import \\([^)]*get_wiki_settings_service"
            ),
            "opennamu_forge/presentation/routes",
            "opennamu_forge/presentation/runtime_app.py",
        ],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 1, result.stdout


@pytest.mark.requires_ripgrep
def test_route와_runtime은_response_helper를_shared_func에서_import하지_않는다():
    result = subprocess.run(
        [
            "rg",
            "-n",
            "-U",
            (
                "from opennamu_forge\\.presentation\\.shared\\.func import "
                "\\([^)]*(get_lang|http_warning|load_domain|load_lang|redirect|render_simple_set|render_template)"
                "|from opennamu_forge\\.presentation\\.shared\\.func import "
                "(get_lang|http_warning|load_domain|load_lang|redirect|render_simple_set|render_template)"
            ),
            "opennamu_forge/presentation/routes",
            "opennamu_forge/presentation/runtime_app.py",
        ],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 1, result.stdout


@pytest.mark.requires_ripgrep
def test_route와_runtime은_text_helper를_shared_func에서_import하지_않는다():
    result = subprocess.run(
        [
            "rg",
            "-n",
            "-U",
            (
                "from opennamu_forge\\.presentation\\.shared\\.func import "
                "\\([^)]*(cache_v|cut_100|get_tool_js_safe|leng_check|load_random_key|number_check)"
                "|from opennamu_forge\\.presentation\\.shared\\.func import "
                "(cache_v|cut_100|get_tool_js_safe|leng_check|load_random_key|number_check)"
            ),
            "opennamu_forge/presentation/routes",
            "opennamu_forge/presentation/runtime_app.py",
        ],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 1, result.stdout


@pytest.mark.requires_ripgrep
def test_route와_runtime은_encoding_helper를_shared_계층에서_import하지_않는다():
    result = subprocess.run(
        [
            "rg",
            "-n",
            "-U",
            (
                "from opennamu_forge\\.presentation\\.shared\\.(func|sql_dialect) import "
                "\\([^)]*(url_pas|sha224_replace|md5_replace|json_dumps|json_loads)"
                "|from opennamu_forge\\.presentation\\.shared\\.(func|sql_dialect) import "
                "(url_pas|sha224_replace|md5_replace|json_dumps|json_loads)"
            ),
            "opennamu_forge/presentation/routes",
            "opennamu_forge/presentation/rendering",
            "opennamu_forge/presentation/runtime",
            "opennamu_forge/presentation/runtime_app.py",
        ],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 1, result.stdout


@pytest.mark.requires_ripgrep
def test_route와_runtime은_startup과_file_helper를_shared_func에서_import하지_않는다():
    result = subprocess.run(
        [
            "rg",
            "-n",
            "-U",
            (
                "from opennamu_forge\\.presentation\\.shared\\.func import "
                "\\([^)]*(linux_exe_chmod|set_init|set_init_always|load_image_url|get_default_robots_txt)"
                "|from opennamu_forge\\.presentation\\.shared\\.func import "
                "(linux_exe_chmod|set_init|set_init_always|load_image_url|get_default_robots_txt)"
            ),
            "opennamu_forge/presentation/routes",
            "opennamu_forge/presentation/runtime_app.py",
        ],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 1, result.stdout


@pytest.mark.requires_ripgrep
def test_route는_ip_pas를_shared_func에서_import하지_않는다():
    result = subprocess.run(
        [
            "rg",
            "-n",
            "-U",
            (
                "from opennamu_forge\\.presentation\\.shared\\.func import "
                "\\([^)]*\\bip_pas\\b"
                "|from opennamu_forge\\.presentation\\.shared\\.func import \\bip_pas\\b"
            ),
            "opennamu_forge/presentation/routes",
        ],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 1, result.stdout


@pytest.mark.requires_ripgrep
def test_route와_runtime은_authorization_helper를_shared_func에서_import하지_않는다():
    result = subprocess.run(
        [
            "rg",
            "-n",
            "-U",
            (
                "from opennamu_forge\\.presentation\\.shared\\.func import "
                "\\([^)]*\\b(acl_check|ban_check|level_check)\\b"
                "|from opennamu_forge\\.presentation\\.shared\\.func import "
                "(acl_check|ban_check|level_check)"
            ),
            "opennamu_forge/presentation/routes",
            "opennamu_forge/presentation/runtime",
        ],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 1, result.stdout


@pytest.mark.requires_ripgrep
def test_route는_email_helper를_shared_func에서_import하지_않는다():
    result = subprocess.run(
        [
            "rg",
            "-n",
            "-U",
            (
                "from opennamu_forge\\.presentation\\.shared\\.func import "
                "\\([^)]*\\bsend_email\\b"
                "|from opennamu_forge\\.presentation\\.shared\\.func import send_email"
            ),
            "opennamu_forge/presentation/routes",
        ],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 1, result.stdout


@pytest.mark.requires_ripgrep
def test_route는_captcha_helper를_shared_func에서_import하지_않는다():
    result = subprocess.run(
        [
            "rg",
            "-n",
            "-U",
            (
                "from opennamu_forge\\.presentation\\.shared\\.func import "
                "\\([^)]*\\b(captcha_get|captcha_post)\\b"
                "|from opennamu_forge\\.presentation\\.shared\\.func import "
                "(captcha_get|captcha_post)"
            ),
            "opennamu_forge/presentation/routes",
        ],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 1, result.stdout


@pytest.mark.requires_ripgrep
def test_route는_user_validation_helper를_shared_func에서_import하지_않는다():
    result = subprocess.run(
        [
            "rg",
            "-n",
            "-U",
            (
                "from opennamu_forge\\.presentation\\.shared\\.func import "
                "\\([^)]*\\bdo_user_name_check\\b"
                "|from opennamu_forge\\.presentation\\.shared\\.func import do_user_name_check"
            ),
            "opennamu_forge/presentation/routes",
        ],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 1, result.stdout
