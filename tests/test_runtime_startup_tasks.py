from types import SimpleNamespace

from opennamu_forge.application.runtime_context import clear_runtime_context, get_runtime_value
from opennamu_forge.presentation.runtime import startup_tasks


class FakeSettings:
    def __init__(self):
        self.values = {
            "wiki_access_password_need": "1",
            "wiki_access_password": "secret",
            "load_ip_select": "HTTP_X_REAL_IP",
        }
        self.writes = []

    def upsert(self, key, value, *args):
        self.values[key] = value
        self.writes.append((key, value))

    def exists(self, key):
        return key in self.values

    def get(self, key, default=""):
        return self.values.get(key, default)

    def list_name_data_by_names(self, names):
        return ()


class FakeAdmins:
    def __init__(self):
        self.groups = []

    def set_group_acls(self, name, acls):
        self.groups.append((name, acls))

    def list_group_names(self):
        return ("owner",)


class FakeBbs:
    def __init__(self):
        self.settings = {}
        self.added = []

    def get_setting(self, bbs_num, key):
        return self.settings.get((bbs_num, key), "")

    def add_setting(self, bbs_num, key, value):
        self.settings[(bbs_num, key)] = value
        self.added.append((bbs_num, key, value))


class FakeHtmlFilters:
    def __init__(self):
        self.inserted = []

    def list_by_kind(self, kind):
        return ()

    def upsert(self, value, kind):
        self.inserted.append((value, kind))


def test_select_go_helper_executable은_linux_x86_바이너리를_반환한다(monkeypatch):
    monkeypatch.setattr(startup_tasks.platform, "system", lambda: "Linux")
    monkeypatch.setattr(startup_tasks.platform, "machine", lambda: "x86_64")

    assert startup_tasks.select_go_helper_executable() == "main.amd64.bin"


def test_select_go_helper_executable은_darwin_바이너리를_반환한다(monkeypatch):
    monkeypatch.setattr(startup_tasks.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(startup_tasks.platform, "machine", lambda: "arm64")

    assert startup_tasks.select_go_helper_executable() == "main.mac.arm64.bin"


def test_initialize_seed_data는_초기_filter와_smtp를_저장한다(monkeypatch):
    html_filters = FakeHtmlFilters()
    settings = FakeSettings()
    monkeypatch.setattr(startup_tasks, "get_html_filter_repository", lambda: html_filters)
    monkeypatch.setattr(startup_tasks, "get_other_setting_repository", lambda: settings)

    startup_tasks.initialize_seed_data()

    assert ("naver.com", "email") in html_filters.inserted
    assert ("webp", "extension") in html_filters.inserted
    assert (r"(?:[^A-Za-zㄱ-ㅣ가-힣0-9])", "name") in html_filters.inserted
    assert ("smtp_server", "smtp.gmail.com") in settings.writes
    assert ("smtp_port", "587") in settings.writes
    assert ("smtp_security", "starttls") in settings.writes


def test_ensure_startup_defaults는_runtime과_기본값을_설정한다(monkeypatch, tmp_path):
    clear_runtime_context()
    settings = FakeSettings()
    admins = FakeAdmins()
    bbs = FakeBbs()
    chmod_calls = []
    image_dir = tmp_path / "images"
    monkeypatch.setattr(startup_tasks, "get_other_setting_repository", lambda: settings)
    monkeypatch.setattr(startup_tasks, "get_admin_repository", lambda: admins)
    monkeypatch.setattr(startup_tasks, "get_bbs_repository", lambda: bbs)
    monkeypatch.setattr(startup_tasks, "load_image_url", lambda: str(image_dir))
    monkeypatch.setattr(startup_tasks, "load_random_key", lambda length=128: "k" * length)
    monkeypatch.setattr(startup_tasks.platform, "system", lambda: "Linux")
    monkeypatch.setattr(startup_tasks.platform, "machine", lambda: "x86_64")
    real_os = startup_tasks.os
    fake_os = SimpleNamespace(
        path=real_os.path,
        makedirs=real_os.makedirs,
        stat=lambda path: type("Stat", (), {"st_mode": 0o644})(),
        chmod=lambda path, mode: chmod_calls.append((path, mode)),
    )
    monkeypatch.setattr(startup_tasks, "os", fake_os)

    startup_tasks.ensure_startup_defaults("123", "dev")

    assert ("ver", "123") in settings.writes
    assert ("user", ("user",)) in admins.groups
    assert ("ip", ("ip",)) in admins.groups
    assert ("ban", ("view",)) in admins.groups
    assert ("0", "bbs_name", "document_comment") in bbs.added
    assert image_dir.exists() is True
    assert get_runtime_value("wiki_access_password") == "secret"
    assert get_runtime_value("load_ip_select") == "HTTP_X_REAL_IP"
    assert chmod_calls == [("bin/main.amd64.bin", 0o755)]
