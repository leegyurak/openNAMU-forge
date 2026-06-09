from __future__ import annotations

import email.mime.text
import smtplib
from collections.abc import Callable
from typing import Any

from opennamu_forge.application.dto.email import SmtpEmailConfig
from opennamu_forge.infrastructure.logging import get_logger

logger = get_logger(__name__)


class SmtpEmailClient:
    def __init__(
        self,
        smtp_factory: Callable[[str, int], Any] = smtplib.SMTP,
        smtp_ssl_factory: Callable[[str, int], Any] = smtplib.SMTP_SSL,
    ):
        self._smtp_factory = smtp_factory
        self._smtp_ssl_factory = smtp_ssl_factory

    def send(self, config: SmtpEmailConfig, to_email: str, title: str, body: str) -> bool:
        try:
            smtp = self._open(config)
            msg = email.mime.text.MIMEText(body)

            msg["Subject"] = title
            msg["From"] = config.wiki_name + " <noreply@" + config.domain + ">"
            msg["To"] = to_email

            smtp.login(config.username, config.password)
            smtp.sendmail("opennamu-forge@" + config.domain, to_email, msg.as_string())
            smtp.quit()
        except Exception:
            logger.exception("Error : email send error")
            return False

        return True

    def _open(self, config: SmtpEmailConfig) -> Any:
        if config.security == "plain":
            return self._smtp_factory(config.server, config.port)

        if config.security == "starttls":
            smtp = self._smtp_factory(config.server, config.port)
            smtp.starttls()
            return smtp

        return self._smtp_ssl_factory(config.server, config.port)
