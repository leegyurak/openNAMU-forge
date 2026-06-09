import asyncio

from opennamu_forge.application.services.challenge_service import ChallengeProgressService
from opennamu_forge.application.services.discussion_service import DiscussionService
from opennamu_forge.application.services.history_service import HistoryMutationService
from opennamu_forge.application.services.main_settings_service import MainSettingsFormService
from opennamu_forge.application.services.recent_change_service import RecentChangeService
from opennamu_forge.application.services.upload_service import UploadPolicyService
from opennamu_forge.application.services.user_registration_service import UserRegistrationService


class FakeOtherSettings:
    def __init__(self, values=None):
        self.values = {} if values is None else values
        self.upserts = []

    def get(self, name, *, coverage="", default=""):
        return self.values.get(name, default)

    def upsert(self, name, data, *, coverage=""):
        self.upserts.append((name, data, coverage))


class FakeMainSettings:
    def __init__(self):
        self.values = None

    def ensure(self, name, *, default="", coverage=""):
        return default

    def set_many(self, values, *, coverage=""):
        self.values = values


class FakeUserSettings:
    def __init__(self, has_any=False):
        self.has_any_value = has_any
        self.adds = []

    def has_any(self):
        return self.has_any_value

    def add(self, user_id, name, data):
        self.adds.append((user_id, name, data))


class FakeHistory:
    def __init__(self):
        self.recent_changes = []
        self.history = []
        self.deleted_recent_changes = []

    def count_recent_changes_by_type(self, change_type):
        return 199

    def oldest_recent_change_ref_by_type(self, change_type):
        return None

    def delete_recent_change(self, title, revision_id, change_type):
        self.deleted_recent_changes.append((title, revision_id, change_type))

    def latest_revision_id(self, title):
        return "2"

    def earliest_revision_id(self, title):
        return "1"

    def add_recent_change(self, title, revision_id, date, change_type):
        self.recent_changes.append((title, revision_id, date, change_type))

    def add_history(self, title, revision_id, data, date, ip, send, length, change_type):
        self.history.append((title, revision_id, data, date, ip, send, length, change_type))


class FakeRecentChangeHistory:
    def __init__(self):
        self.calls = []

    def list_records_by_title(self, title, *, offset=0, limit=50):
        self.calls.append(("title", title, offset, limit))
        return ["title-record"]

    def list_records_by_title_type(self, title, change_type, *, offset=0, limit=50):
        self.calls.append(("title-type", title, change_type, offset, limit))
        return ["title-type-record"]

    def list_records_by_ip(self, ip, *, offset=0, limit=50):
        self.calls.append(("ip", ip, offset, limit))
        return ["ip-record"]

    def list_records_by_ip_type(self, ip, change_type, *, offset=0, limit=50):
        self.calls.append(("ip-type", ip, change_type, offset, limit))
        return ["ip-type-record"]

    def list_recent_change_records_by_type(self, change_type, *, limit=50):
        self.calls.append(("recent-type", change_type, limit))
        return ["recent-record"]

    def list_records_by_type(self, change_type, *, offset=0, limit=50):
        self.calls.append(("all-type", change_type, offset, limit))
        return ["all-type-record"]

    def list_records(self, *, offset=0, limit=50):
        self.calls.append(("all", offset, limit))
        return ["all-record"]


class FakeDocumentMeta:
    def __init__(self):
        self.deleted = []
        self.upserts = []
        self.revision_markers = []

    def delete(self, doc_name, set_name, *, doc_rev=""):
        self.deleted.append((doc_name, set_name, doc_rev))

    def upsert(self, doc_name, set_name, set_data, *, doc_rev=""):
        self.upserts.append((doc_name, set_name, set_data, doc_rev))

    def update_revision_marker(self, doc_name, doc_rev):
        self.revision_markers.append((doc_name, doc_rev))


class FakeWikiDocuments:
    def count_all_titles(self):
        return 7


class FakeTopics:
    def __init__(self):
        self.comments = []
        self.recent_discussions = []
        self.updated_recent = False

    def latest_comment_id(self, code):
        return 4

    def add_comment(self, code, comment_id, data, date, ip, block, *, top=""):
        self.comments.append((code, comment_id, data, date, ip, block, top))

    def update_recent_discuss_date(self, code, date):
        return self.updated_recent

    def add_recent_discuss(self, code, title, subtitle, date):
        self.recent_discussions.append((code, title, subtitle, date))


class FakeChallengeHistory:
    def __init__(self, count):
        self.count = count

    def count_by_ip(self, ip):
        return self.count


class FakeChallengeTopics:
    def __init__(self, count):
        self.count = count

    def count_by_ip(self, ip):
        return self.count


class FakeChallengeUserSettings:
    def __init__(self, has_admin=False):
        self.has_admin = has_admin
        self.upserts = []

    def exists(self, user_id, name):
        return self.has_admin if name == "challenge_admin" else False

    def upsert(self, user_id, name, data):
        self.upserts.append((user_id, name, data))


class FakeAlarms:
    def __init__(self):
        self.sent = []

    async def send_alarm(self, to_user, from_user, context):
        self.sent.append((to_user, from_user, context))


def test_user_registration_service는_첫_사용자를_owner로_생성한다():
    users = FakeUserSettings()
    service = UserRegistrationService(
        users,
        FakeOtherSettings({"encode": "sha3"}),
        lambda password: "hashed:" + password,
        lambda: "2026-06-09 12:00:00",
    )

    service.add_user("alice", "pw", "alice@example.test")

    assert users.adds == [
        ("alice", "pw", "hashed:pw"),
        ("alice", "acl", "owner"),
        ("alice", "date", "2026-06-09 12:00:00"),
        ("alice", "encode", "sha3"),
        ("alice", "email", "alice@example.test"),
    ]


def test_main_settings_form_service는_기본값과_secret_key를_로드한다():
    service = MainSettingsFormService(FakeMainSettings(), lambda: "secret-key")

    values = service.load_form_values()

    assert values[0] == "Wiki"
    assert values[11] == "secret-key"
    assert values[15] == "sha3"


def test_main_settings_form_service는_form값을_저장한다():
    settings = FakeMainSettings()
    service = MainSettingsFormService(settings, lambda: "secret-key")

    service.update_from_form({"name": "Forge"})

    assert settings.values is not None
    assert settings.values["name"] == "Forge"
    assert settings.values["key"] == "secret-key"


def test_user_registration_service는_encoded_password를_그대로_저장한다():
    users = FakeUserSettings(has_any=True)
    service = UserRegistrationService(
        users,
        FakeOtherSettings({"encode": "sha3"}),
        lambda password: "hashed:" + password,
        lambda: "2026-06-09 12:00:00",
    )

    service.add_user("bob", "already-hashed", user_encode="legacy")

    assert users.adds == [
        ("bob", "pw", "already-hashed"),
        ("bob", "acl", "user"),
        ("bob", "date", "2026-06-09 12:00:00"),
        ("bob", "encode", "legacy"),
    ]


def test_history_mutation_service는_revision과_recent_change를_기록한다():
    history = FakeHistory()
    document_meta = FakeDocumentMeta()
    other_settings = FakeOtherSettings()
    service = HistoryMutationService(history, document_meta, other_settings, FakeWikiDocuments())

    service.add_history("FrontPage", "body", "2026-06-09 12:00:00", "alice", "<send>", "4", mode="edit")

    assert history.recent_changes == [
        ("FrontPage", "3", "2026-06-09 12:00:00", "normal"),
        ("FrontPage", "3", "2026-06-09 12:00:00", "edit"),
    ]
    assert history.history == [("FrontPage", "3", "body", "2026-06-09 12:00:00", "alice", "send", "4", "edit")]
    assert other_settings.upserts == [("count_all_title", "7", "")]
    assert document_meta.revision_markers == [("FrontPage", "")]


def test_recent_change_service는_history_view_조회를_repository에_위임한다():
    history = FakeRecentChangeHistory()
    service = RecentChangeService(history)

    result = service.list_records("FrontPage", "history", 2, "edit", can_page_all=True)

    assert result.records == ["title-type-record"]
    assert result.normalized_set_type == ""
    assert history.calls == [("title-type", "FrontPage", "", 50, 50)]


def test_recent_change_service는_admin이_아니면_recent_records를_사용한다():
    history = FakeRecentChangeHistory()
    service = RecentChangeService(history)

    result = service.list_records("", "", 3, "normal", can_page_all=False)

    assert result.records == ["recent-record"]
    assert history.calls == [("recent-type", "normal", 50)]


def test_upload_policy_service는_용량과_다중업로드_정책을_계산한다():
    service = UploadPolicyService()

    assert service.normalize_content_length(None) == 0
    assert service.is_size_invalid(2, 1, 0) is True
    assert service.is_size_invalid(2, 1, 1000) is False
    assert service.initial_file_number(1, can_many_upload=False) is None
    assert service.initial_file_number(2, can_many_upload=True) == 1
    assert service.initial_file_number(2, can_many_upload=False) == 0


def test_upload_policy_service는_file_document_text를_생성한다():
    service = UploadPolicyService()

    assert service.build_upload_title("cat.png", "logo", 2, ".png") == "logo 2.png"
    assert service.build_file_document_text("namumark", "license]", "memo") == "license]\n[[category:license_]]\nmemo"
    assert service.build_file_document_text("markdown", "license", "") == "license\n"


def test_discussion_service는_thread_comment와_recent_thread를_기록한다():
    topics = FakeTopics()
    service = DiscussionService(topics, FakeAlarms(), lambda: "2026-06-09 12:00:00", lambda: "alice")

    service.add_thread_comment("T1", "hello", "1")
    service.reload_recent_thread("T1", "2026-06-09 12:00:01", "FrontPage", "Question")

    assert topics.comments == [("T1", "5", "hello", "2026-06-09 12:00:00", "alice", "1", "")]
    assert topics.recent_discussions == [("T1", "FrontPage", "Question", "2026-06-09 12:00:01")]


def test_discussion_service는_alarm_port를_사용한다():
    alarms = FakeAlarms()
    service = DiscussionService(FakeTopics(), alarms, lambda: "2026-06-09 12:00:00", lambda: "alice")

    asyncio.run(service.add_alarm("bob", "alice", "context"))

    assert alarms.sent == [("bob", "alice", "context")]


def test_challenge_progress_service는_기여_보상과_level을_저장한다():
    users = FakeChallengeUserSettings()
    service = ChallengeProgressService(FakeChallengeHistory(1), FakeChallengeTopics(0), users)

    progress = service.refresh_user_progress("alice", 1)

    assert progress.level == 1
    assert progress.experience == 5
    assert progress.history_count == 1
    assert progress.topic_count == 0
    assert users.upserts == [
        ("alice", "challenge_first_contribute", "1"),
        ("alice", "level", "1"),
        ("alice", "experience", "5"),
    ]


def test_challenge_progress_service는_admin_challenge를_기존_달성자에게_유지한다():
    users = FakeChallengeUserSettings(has_admin=True)
    service = ChallengeProgressService(FakeChallengeHistory(0), FakeChallengeTopics(0), users)

    progress = service.refresh_user_progress("alice", 1)

    assert progress.level == 12
    assert progress.experience == 700
    assert users.upserts == [
        ("alice", "challenge_admin", "1"),
        ("alice", "level", "12"),
        ("alice", "experience", "700"),
    ]
