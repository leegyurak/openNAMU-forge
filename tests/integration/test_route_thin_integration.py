import importlib

import flask

from opennamu_forge.application.services.recent_change_service import RecentChangeQueryResult

recent_change_module = importlib.import_module("opennamu_forge.presentation.routes.recent_change")
user_challenge_module = importlib.import_module("opennamu_forge.presentation.routes.user_challenge")


class FakeChallengeProgress:
    def __init__(self):
        self.calls = []

    def refresh_user_progress(self, user_id, admin_acl_result):
        self.calls.append((user_id, admin_acl_result))


class FakeUserSettings:
    def exists(self, user_id, name):
        return False


class FakeRecentChangeService:
    def list_records(self, name, tool, num, set_type, *, can_page_all):
        return RecentChangeQueryResult([], set_type)


def test_user_challenge_route는_post에서_progress_service를_호출한다(monkeypatch):
    progress = FakeChallengeProgress()
    app = flask.Flask(__name__)
    app.secret_key = "test"
    app.add_url_rule("/challenge", view_func=user_challenge_module.user_challenge, methods=["POST"])

    async def fake_acl_check(*args, **kwargs):
        return 1

    monkeypatch.setattr(user_challenge_module, "acl_check", fake_acl_check)
    monkeypatch.setattr(user_challenge_module, "get_challenge_progress_service", lambda: progress)
    monkeypatch.setattr(user_challenge_module, "ip_check", lambda: "alice")
    monkeypatch.setattr(user_challenge_module, "ip_or_user", lambda ip: 0)
    monkeypatch.setattr(user_challenge_module, "redirect", flask.redirect)

    response = app.test_client().post("/challenge")

    assert response.status_code == 302
    assert response.headers["Location"] == "/challenge"
    assert progress.calls == [("alice", 1)]


def test_recent_change_route는_service_결과로_template을_렌더링한다(monkeypatch):
    app = flask.Flask(__name__)
    app.secret_key = "test"
    app.add_url_rule("/recent_change", view_func=recent_change_module.recent_change, methods=["GET"])

    async def fake_acl_check(*args, **kwargs):
        return 1

    async def fake_get_lang(data, safe=0):
        return data

    async def fake_render_template(title, body, sub, menu, *args, **kwargs):
        return title + "|" + str(sub) + "|" + str(menu) + "|" + body

    async def fake_ip_pas(raw_ip):
        return {}

    monkeypatch.setattr(recent_change_module, "acl_check", fake_acl_check)
    monkeypatch.setattr(recent_change_module, "get_recent_change_service", lambda: FakeRecentChangeService())
    monkeypatch.setattr(recent_change_module, "get_lang", fake_get_lang)
    monkeypatch.setattr(recent_change_module, "ip_check", lambda: "alice")
    monkeypatch.setattr(recent_change_module, "ip_pas", fake_ip_pas)
    monkeypatch.setattr(recent_change_module, "render_template", fake_render_template)

    response = app.test_client().get("/recent_change")

    assert response.status_code == 200
    assert b"recent_change" in response.data
    assert b"main_table_set" in response.data
