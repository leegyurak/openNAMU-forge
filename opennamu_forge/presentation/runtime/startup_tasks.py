from __future__ import annotations

import os
import platform

from opennamu_forge.application.runtime_context import set_runtime_value
from opennamu_forge.presentation.dependencies import (
    get_admin_repository,
    get_bbs_repository,
    get_html_filter_repository,
    get_other_setting_repository,
)
from opennamu_forge.presentation.file_helpers import load_image_url
from opennamu_forge.presentation.text_helpers import load_random_key


def select_go_helper_executable() -> str:
    exe_type = ""
    if platform.system() == "Linux":
        if platform.machine() in ["AMD64", "x86_64"]:
            exe_type = "main.amd64.bin"
        else:
            exe_type = "main.arm64.bin"
    elif platform.system() == "Darwin":
        exe_type = "main.mac.arm64.bin"
    else:
        if platform.machine() in ["AMD64", "x86_64"]:
            exe_type = "main.amd64.exe"
        else:
            exe_type = "main.arm64.exe"

    return exe_type


def ensure_startup_defaults(ver_num: str, run_mode: str) -> None:
    settings = get_other_setting_repository()
    admins = get_admin_repository()

    settings.upsert("ver", ver_num)

    admins.set_group_acls("owner", ("owner",))

    if "user" not in admins.list_group_names():
        admins.set_group_acls("user", ("user",))

    if "ip" not in admins.list_group_names():
        admins.set_group_acls("ip", ("ip",))

    if "ban" not in admins.list_group_names():
        admins.set_group_acls("ban", ("view",))

    bbs_num = "0"
    bbs_name = "document_comment"
    bbs_type = "comment"
    bbs = get_bbs_repository()

    if bbs.get_setting(bbs_num, "bbs_name") == "":
        bbs.add_setting(bbs_num, "bbs_name", bbs_name)

    if bbs.get_setting(bbs_num, "bbs_type") == "":
        bbs.add_setting(bbs_num, "bbs_type", bbs_type)

    if not os.path.exists(load_image_url()):
        os.makedirs(load_image_url())

    if not settings.exists("key"):
        settings.upsert("key", load_random_key())

    if not settings.exists("salt_key"):
        settings.upsert("salt_key", load_random_key(4))

    if not settings.exists("count_all_title"):
        settings.upsert("count_all_title", "0")

    db_data = settings.get("wiki_access_password_need")
    if db_data != "":
        wiki_access_password = settings.get("wiki_access_password")
        if wiki_access_password != "":
            set_runtime_value("wiki_access_password", wiki_access_password)

    db_data = settings.get("load_ip_select")
    if db_data != "":
        set_runtime_value("load_ip_select", db_data)

    exe_type = select_go_helper_executable()
    if platform.system() == "Linux" or platform.system() == "Darwin":
        executable_path = os.path.join("bin", exe_type)
        try:
            os.chmod(executable_path, os.stat(executable_path).st_mode | 0o111)
        except FileNotFoundError:
            pass


def initialize_seed_data() -> None:
    html_filters = get_html_filter_repository()
    settings = get_other_setting_repository()

    if not html_filters.list_by_kind("email"):
        for domain in ["naver.com", "gmail.com", "daum.net", "kakao.com"]:
            html_filters.upsert(domain, "email")

    if not html_filters.list_by_kind("extension"):
        for extension in ["jpg", "jpeg", "png", "gif", "webp"]:
            html_filters.upsert(extension, "extension")

    if not settings.list_name_data_by_names(("smtp_server", "smtp_port", "smtp_security")):
        for name, value in [["smtp_server", "smtp.gmail.com"], ["smtp_port", "587"], ["smtp_security", "starttls"]]:
            settings.upsert(name, value)

    html_filters.upsert(r"(?:[^A-Za-zㄱ-ㅣ가-힣0-9])", "name")
