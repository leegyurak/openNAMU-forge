import asyncio
from types import SimpleNamespace

from opennamu_forge.presentation.runtime import scheduler


class FakeSettings:
    def __init__(self, values):
        self.values = values

    def get(self, key):
        return self.values.get(key, "")


class FakeVotes:
    def __init__(self):
        self.updates = []

    def list_by_types(self, types, limit):
        return (
            SimpleNamespace(vote_id="1", type="open"),
            SimpleNamespace(vote_id="2", type="n_open"),
        )

    def get_option(self, vote_id, key):
        return "2026-06-08 00:00:00"

    def update_main_type(self, vote_id, old_type, new_type):
        self.updates.append((vote_id, old_type, new_type))


class FakeUserSettings:
    def __init__(self):
        self.upserts = []
        self.deletes = []
        self.updated_titles = []

    def list_id_data_by_name(self, name):
        return (("user", "2026-06-08 00:00:00"),)

    def upsert(self, user_id, key, value):
        self.upserts.append((user_id, key, value))

    def delete(self, user_id, key):
        self.deletes.append((user_id, key))

    def list_ids_by_name_data(self, name, data):
        return ("admin",)

    def update_user_title_checkmark(self, user_id):
        self.updated_titles.append(user_id)


class FakeDocumentMeta:
    def __init__(self):
        self.deleted_acl = []
        self.deleted_meta = []

    def list_doc_rev_data_by_set_name(self, name):
        return (("FrontPage", "7", "2026-06-08 00:00:00"),)

    def delete_acl(self, title, rev):
        self.deleted_acl.append((title, rev))

    def delete(self, title, key, doc_rev=None):
        self.deleted_meta.append((title, key, doc_rev))


class FakeRecentBlocks:
    def __init__(self):
        self.closed_at = ""

    def close_expired(self, now):
        self.closed_at = now


class FakeUserAgents:
    def __init__(self):
        self.deleted_before = ""

    def delete_older_than(self, time_calc):
        self.deleted_before = time_calc


class FakeAdmins:
    def __init__(self):
        self.deleted_before = ""

    def delete_records_older_than(self, time_calc):
        self.deleted_before = time_calc


class FakeTimer:
    started = False
    args = None

    def __init__(self, seconds, callback, args):
        self.seconds = seconds
        self.callback = callback
        self.args = args

    def start(self):
        FakeTimer.started = True
        FakeTimer.args = (self.seconds, self.callback, self.args)


def test_do_every_day는_만료된_런타임_작업을_처리한다(monkeypatch):
    votes = FakeVotes()
    user_settings = FakeUserSettings()
    document_meta = FakeDocumentMeta()
    recent_blocks = FakeRecentBlocks()
    user_agents = FakeUserAgents()
    admins = FakeAdmins()
    sitemap_calls = []

    async def fake_acl_check(name, tool, topic_num, ip):
        return 1

    async def fake_sitemap():
        sitemap_calls.append(1)

    monkeypatch.setattr(scheduler, "get_time", lambda: "2026-06-09 00:00:00")
    monkeypatch.setattr(
        scheduler,
        "get_other_setting_repository",
        lambda: FakeSettings(
            {
                "ua_expiration_date": "3",
                "auth_history_expiration_date": "4",
                "sitemap_auto_make": "1",
            }
        ),
    )
    monkeypatch.setattr(scheduler, "get_vote_repository", lambda: votes)
    monkeypatch.setattr(scheduler, "get_user_setting_repository", lambda: user_settings)
    monkeypatch.setattr(scheduler, "get_document_meta_repository", lambda: document_meta)
    monkeypatch.setattr(scheduler, "get_recent_block_repository", lambda: recent_blocks)
    monkeypatch.setattr(scheduler, "get_user_agent_repository", lambda: user_agents)
    monkeypatch.setattr(scheduler, "get_admin_repository", lambda: admins)
    monkeypatch.setattr(scheduler, "acl_check", fake_acl_check)
    monkeypatch.setattr(scheduler, "make_auto_sitemap", fake_sitemap)

    asyncio.run(scheduler.do_every_day())

    assert votes.updates == [("1", "open", "close"), ("2", "n_open", "n_close")]
    assert recent_blocks.closed_at == "2026-06-09 00:00:00"
    assert user_settings.upserts == [("user", "acl", "user")]
    assert user_settings.deletes == [("user", "auth_date")]
    assert document_meta.deleted_acl == [("FrontPage", "7")]
    assert document_meta.deleted_meta == [("FrontPage", "acl_date", "7")]
    assert user_agents.deleted_before != ""
    assert admins.deleted_before != ""
    assert sitemap_calls == [1]
    assert user_settings.updated_titles == ["admin"]


def test_back_up은_기존_백업을_정리하고_새_백업을_만든다(monkeypatch, tmp_path):
    db_file = tmp_path / "wiki.db"
    backup_file = tmp_path / "wiki_20260101000000.db"
    db_file.write_text("current", encoding="utf-8")
    backup_file.write_text("old", encoding="utf-8")
    FakeTimer.started = False
    FakeTimer.args = None

    monkeypatch.setattr(
        scheduler,
        "get_other_setting_repository",
        lambda: FakeSettings(
            {
                "back_up": "1",
                "backup_count": "1",
                "backup_where": str(db_file),
            }
        ),
    )
    monkeypatch.setattr(scheduler.threading, "Timer", FakeTimer)

    scheduler.back_up({"type": "sqlite", "name": str(tmp_path / "wiki")})

    assert backup_file.exists() is False
    assert FakeTimer.started is True
    assert FakeTimer.args[1] is scheduler.back_up


def test_auto_do_something은_sqlite에서_backup과_scheduler를_시작한다(monkeypatch):
    calls = []

    monkeypatch.setattr(scheduler, "back_up", lambda data_db_set: calls.append(("backup", data_db_set["type"])))
    monkeypatch.setattr(scheduler, "start_daily_scheduler", lambda: calls.append(("daily", "")))

    scheduler.auto_do_something({"type": "sqlite"})

    assert calls == [("backup", "sqlite"), ("daily", "")]
