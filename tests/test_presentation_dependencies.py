import pytest

from opennamu_forge.application.runtime_context import clear_runtime_context
from opennamu_forge.application.services.settings_service import WikiSettingsService
from opennamu_forge.config.runtime_database import apply_database_runtime_config
from opennamu_forge.infrastructure.admin_repository import AdminRepository
from opennamu_forge.infrastructure.backlink_repository import BacklinkRepository
from opennamu_forge.infrastructure.bbs_repository import BbsRepository
from opennamu_forge.infrastructure.captcha_client import AiohttpCaptchaClient
from opennamu_forge.infrastructure.document_meta_repository import DocumentMetaRepository
from opennamu_forge.infrastructure.history_repository import HistoryRepository
from opennamu_forge.infrastructure.html_filter_repository import HtmlFilterRepository
from opennamu_forge.infrastructure.recent_block_repository import RecentBlockRepository
from opennamu_forge.infrastructure.setting_repository import OtherSettingRepository
from opennamu_forge.infrastructure.smtp_email_client import SmtpEmailClient
from opennamu_forge.infrastructure.topic_repository import TopicRepository
from opennamu_forge.infrastructure.user_agent_repository import UserAgentDataRepository
from opennamu_forge.infrastructure.user_notice_repository import UserNoticeRepository
from opennamu_forge.infrastructure.user_setting_repository import UserSettingRepository
from opennamu_forge.infrastructure.vote_repository import VoteRepository
from opennamu_forge.infrastructure.wiki_repository import WikiDocumentRepository
from opennamu_forge.presentation import dependencies


@pytest.fixture(autouse=True)
def test_runtime_database_config를_초기화한다(tmp_path):
    clear_runtime_context()
    apply_database_runtime_config({"type": "sqlite", "name": str(tmp_path / "dependencies")})
    yield
    clear_runtime_context()


@pytest.mark.parametrize(
    ("factory", "expected_type"),
    [
        (dependencies.get_other_setting_repository, OtherSettingRepository),
        (dependencies.get_admin_repository, AdminRepository),
        (dependencies.get_html_filter_repository, HtmlFilterRepository),
        (dependencies.get_bbs_repository, BbsRepository),
        (dependencies.get_backlink_repository, BacklinkRepository),
        (dependencies.get_recent_block_repository, RecentBlockRepository),
        (dependencies.get_wiki_document_repository, WikiDocumentRepository),
        (dependencies.get_document_meta_repository, DocumentMetaRepository),
        (dependencies.get_user_setting_repository, UserSettingRepository),
        (dependencies.get_user_agent_repository, UserAgentDataRepository),
        (dependencies.get_user_notice_repository, UserNoticeRepository),
        (dependencies.get_vote_repository, VoteRepository),
        (dependencies.get_topic_repository, TopicRepository),
        (dependencies.get_history_repository, HistoryRepository),
    ],
)
def test_repository_provider는_현재_runtime_db_config로_repository를_생성한다(factory, expected_type):
    repository = factory()

    assert isinstance(repository, expected_type)
    assert repository.db_set["type"] == "sqlite"


def test_wiki_settings_service_provider는_other_setting_repository를_사용한다():
    service = dependencies.get_wiki_settings_service()

    assert isinstance(service, WikiSettingsService)
    assert isinstance(service.settings, OtherSettingRepository)


def test_email_client_provider는_smtp_email_client를_생성한다():
    client = dependencies.get_email_client()

    assert isinstance(client, SmtpEmailClient)


def test_captcha_client_provider는_aiohttp_captcha_client를_생성한다():
    client = dependencies.get_captcha_client()

    assert isinstance(client, AiohttpCaptchaClient)
