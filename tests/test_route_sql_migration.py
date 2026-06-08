from pathlib import Path

import pytest

ROUTE_FILES = tuple(Path("opennamu_forge/presentation/routes").glob("*.py"))


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
        "opennamu_forge/presentation/routes/edit_move.py",
        "opennamu_forge/presentation/routes/login_register_submit.py",
        "opennamu_forge/presentation/routes/main_sys_update.py",
        "opennamu_forge/presentation/routes/recent_app_submit.py",
        "opennamu_forge/presentation/routes/recent_history_send.py",
        "opennamu_forge/presentation/routes/topic_comment_blind.py",
        "opennamu_forge/presentation/routes/topic_comment_delete.py",
        "opennamu_forge/presentation/routes/topic_comment_notice.py",
        "opennamu_forge/presentation/routes/user_challenge.py",
        "opennamu_forge/presentation/routes/user_setting_skin_set.py",
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
