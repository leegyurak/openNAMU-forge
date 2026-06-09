import asyncio

from opennamu_forge.application.dto.email import SmtpEmailConfig
from opennamu_forge.presentation import email_helpers


class FakeSettings:
    def list_name_data_by_names(self, names):
        return [
            ("smtp_email", "user"),
            ("smtp_pass", "pass"),
            ("smtp_server", "smtp.example.com"),
            ("smtp_port", "587"),
            ("smtp_security", "starttls"),
            ("name", "Forge Wiki"),
        ]


class FakeEmailClient:
    def __init__(self, sent):
        self.sent = sent
        self.calls = []

    def send(self, config, who, title, data):
        self.calls.append((config, who, title, data))
        return self.sent


def test_send_email은_smtp_config를_조립해_client에_전달한다(monkeypatch):
    client = FakeEmailClient(True)
    monkeypatch.setattr(email_helpers, "get_other_setting_repository", lambda: FakeSettings())
    monkeypatch.setattr(email_helpers, "get_email_client", lambda: client)
    monkeypatch.setattr(email_helpers, "load_domain", lambda: "wiki.example.com")

    result = asyncio.run(email_helpers.send_email("to@example.com", "Title", "Body"))

    assert result == 1
    assert client.calls == [
        (
            SmtpEmailConfig(
                username="user",
                password="pass",
                server="smtp.example.com",
                port=587,
                security="starttls",
                domain="wiki.example.com",
                wiki_name="Forge Wiki",
            ),
            "to@example.com",
            "Title",
            "Body",
        )
    ]


def test_send_email은_client_실패시_0을_반환한다(monkeypatch):
    client = FakeEmailClient(False)
    monkeypatch.setattr(email_helpers, "get_other_setting_repository", lambda: FakeSettings())
    monkeypatch.setattr(email_helpers, "get_email_client", lambda: client)
    monkeypatch.setattr(email_helpers, "load_domain", lambda: "wiki.example.com")

    result = asyncio.run(email_helpers.send_email("to@example.com", "Title", "Body"))

    assert result == 0
