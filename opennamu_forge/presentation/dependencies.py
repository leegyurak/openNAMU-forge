from __future__ import annotations

from opennamu_forge.application.ports.captcha import CaptchaClientPort
from opennamu_forge.application.ports.email import EmailClientPort
from opennamu_forge.application.ports.repositories import (
    AdminPort,
    BacklinkPort,
    BbsPort,
    DocumentMetaPort,
    HistoryPort,
    HtmlFilterPort,
    OtherSettingPort,
    RecentBlockPort,
    TopicPort,
    UserAgentDataPort,
    UserNoticePort,
    UserSettingPort,
    VotePort,
    WikiDocumentPort,
)
from opennamu_forge.application.ports.skin_info import SkinInfoClientPort
from opennamu_forge.application.services.settings_service import WikiSettingsService
from opennamu_forge.config.runtime_database import get_current_db_set
from opennamu_forge.infrastructure.admin_repository import AdminRepository
from opennamu_forge.infrastructure.backlink_repository import BacklinkRepository
from opennamu_forge.infrastructure.bbs_repository import BbsRepository
from opennamu_forge.infrastructure.captcha_client import AiohttpCaptchaClient
from opennamu_forge.infrastructure.document_meta_repository import DocumentMetaRepository
from opennamu_forge.infrastructure.history_repository import HistoryRepository
from opennamu_forge.infrastructure.html_filter_repository import HtmlFilterRepository
from opennamu_forge.infrastructure.recent_block_repository import RecentBlockRepository
from opennamu_forge.infrastructure.setting_repository import OtherSettingRepository
from opennamu_forge.infrastructure.skin_info_client import SkinInfoClient
from opennamu_forge.infrastructure.smtp_email_client import SmtpEmailClient
from opennamu_forge.infrastructure.topic_repository import TopicRepository
from opennamu_forge.infrastructure.user_agent_repository import UserAgentDataRepository
from opennamu_forge.infrastructure.user_notice_repository import UserNoticeRepository
from opennamu_forge.infrastructure.user_setting_repository import UserSettingRepository
from opennamu_forge.infrastructure.vote_repository import VoteRepository
from opennamu_forge.infrastructure.wiki_repository import WikiDocumentRepository


def get_other_setting_repository() -> OtherSettingPort:
    return OtherSettingRepository(get_current_db_set())

def get_admin_repository() -> AdminPort:
    return AdminRepository(get_current_db_set())

def get_html_filter_repository() -> HtmlFilterPort:
    return HtmlFilterRepository(get_current_db_set())

def get_bbs_repository() -> BbsPort:
    return BbsRepository(get_current_db_set())

def get_backlink_repository() -> BacklinkPort:
    return BacklinkRepository(get_current_db_set())

def get_recent_block_repository() -> RecentBlockPort:
    return RecentBlockRepository(get_current_db_set())

def get_wiki_settings_service() -> WikiSettingsService:
    return WikiSettingsService(get_other_setting_repository())

def get_wiki_document_repository() -> WikiDocumentPort:
    return WikiDocumentRepository(get_current_db_set())

def get_document_meta_repository() -> DocumentMetaPort:
    return DocumentMetaRepository(get_current_db_set())

def get_user_setting_repository() -> UserSettingPort:
    return UserSettingRepository(get_current_db_set())

def get_user_agent_repository() -> UserAgentDataPort:
    return UserAgentDataRepository(get_current_db_set())

def get_user_notice_repository() -> UserNoticePort:
    return UserNoticeRepository(get_current_db_set())

def get_vote_repository() -> VotePort:
    return VoteRepository(get_current_db_set())

def get_topic_repository() -> TopicPort:
    return TopicRepository(get_current_db_set())

def get_history_repository() -> HistoryPort:
    return HistoryRepository(get_current_db_set())

def get_skin_info_client() -> SkinInfoClientPort:
    return SkinInfoClient()

def get_email_client() -> EmailClientPort:
    return SmtpEmailClient()

def get_captcha_client() -> CaptchaClientPort:
    return AiohttpCaptchaClient()
