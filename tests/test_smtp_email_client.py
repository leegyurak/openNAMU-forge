from opennamu_forge.application.dto.email import SmtpEmailConfig
from opennamu_forge.infrastructure.smtp_email_client import SmtpEmailClient


class FakeSmtp:
    def __init__(self):
        self.started_tls = False
        self.logged_in = None
        self.sent = None
        self.closed = False

    def starttls(self):
        self.started_tls = True

    def login(self, username, password):
        self.logged_in = (username, password)

    def sendmail(self, from_email, to_email, body):
        self.sent = (from_email, to_email, body)

    def quit(self):
        self.closed = True


def test_smtp_email_client는_plain_smtp로_메일을_전송한다():
    smtp = FakeSmtp()
    client = SmtpEmailClient(
        smtp_factory=lambda server, port: smtp,
        smtp_ssl_factory=lambda server, port: FakeSmtp(),
    )

    sent = client.send(
        SmtpEmailConfig(
            username="user",
            password="pass",
            server="smtp.example.com",
            port=25,
            security="plain",
            domain="wiki.example.com",
            wiki_name="Forge Wiki",
        ),
        "to@example.com",
        "Title",
        "Body",
    )

    assert sent is True
    assert smtp.started_tls is False
    assert smtp.logged_in == ("user", "pass")
    assert smtp.sent is not None
    assert smtp.sent[0] == "opennamu-forge@wiki.example.com"
    assert smtp.sent[1] == "to@example.com"
    assert "Title" in smtp.sent[2]
    assert smtp.closed is True


def test_smtp_email_client는_starttls를_시작한다():
    smtp = FakeSmtp()
    client = SmtpEmailClient(
        smtp_factory=lambda server, port: smtp,
        smtp_ssl_factory=lambda server, port: FakeSmtp(),
    )

    client.send(
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

    assert smtp.started_tls is True


def test_smtp_email_client는_tls면_ssl_factory를_사용한다():
    smtp = FakeSmtp()
    plain_smtp = FakeSmtp()
    client = SmtpEmailClient(
        smtp_factory=lambda server, port: plain_smtp,
        smtp_ssl_factory=lambda server, port: smtp,
    )

    client.send(
        SmtpEmailConfig(
            username="user",
            password="pass",
            server="smtp.example.com",
            port=465,
            security="tls",
            domain="wiki.example.com",
            wiki_name="Forge Wiki",
        ),
        "to@example.com",
        "Title",
        "Body",
    )

    assert smtp.logged_in == ("user", "pass")
    assert plain_smtp.logged_in is None


def test_smtp_email_client는_전송_실패시_false를_반환한다():
    def failing_factory(server, port):
        raise OSError

    client = SmtpEmailClient(
        smtp_factory=failing_factory,
        smtp_ssl_factory=lambda server, port: FakeSmtp(),
    )

    sent = client.send(
        SmtpEmailConfig(
            username="user",
            password="pass",
            server="smtp.example.com",
            port=25,
            security="plain",
            domain="wiki.example.com",
            wiki_name="Forge Wiki",
        ),
        "to@example.com",
        "Title",
        "Body",
    )

    assert sent is False
