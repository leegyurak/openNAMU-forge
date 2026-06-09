from __future__ import annotations

from opennamu_forge.application.dto.email import SmtpEmailConfig
from opennamu_forge.presentation.dependencies import (
    get_email_client,
    get_other_setting_repository,
)
from opennamu_forge.presentation.response_helpers import load_domain
from opennamu_forge.presentation.text_helpers import number_check


async def send_email(who: str, title: str, data: str) -> int:
    rep_data = dict(
        get_other_setting_repository().list_name_data_by_names(
            (
                "smtp_email",
                "smtp_pass",
                "smtp_server",
                "smtp_port",
                "smtp_security",
                "name",
            )
        )
    )
    config = SmtpEmailConfig(
        username=rep_data.get("smtp_email", ""),
        password=rep_data.get("smtp_pass", ""),
        server=rep_data.get("smtp_server", ""),
        port=int(number_check(rep_data.get("smtp_port", ""))),
        security=rep_data.get("smtp_security", ""),
        domain=load_domain(),
        wiki_name=rep_data.get("name", "Wiki"),
    )
    sent = get_email_client().send(config, who, title, data)

    return 1 if sent else 0
