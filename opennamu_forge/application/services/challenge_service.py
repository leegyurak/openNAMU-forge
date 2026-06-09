from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class ChallengeHistoryStore(Protocol):
    def count_by_ip(self, ip: str) -> int: ...


class ChallengeTopicStore(Protocol):
    def count_by_ip(self, ip: str) -> int: ...


class ChallengeUserSettings(Protocol):
    def exists(self, user_id: str, name: str) -> bool: ...
    def upsert(self, user_id: str, name: str, data: str) -> None: ...


@dataclass(frozen=True)
class ChallengeProgress:
    level: int
    experience: int
    history_count: int
    topic_count: int


@dataclass(frozen=True)
class ChallengeProgressService:
    histories: ChallengeHistoryStore
    topics: ChallengeTopicStore
    user_settings: ChallengeUserSettings

    def refresh_user_progress(self, user_id: str, admin_acl_result: int) -> ChallengeProgress:
        user_exp = 0

        history_count = self.histories.count_by_ip(user_id)
        user_exp += 5 * history_count
        user_exp += self._upsert_history_challenges(user_id, history_count)

        topic_count = self.topics.count_by_ip(user_id)
        user_exp += 5 * topic_count
        user_exp += self._upsert_topic_challenges(user_id, topic_count)

        if admin_acl_result != 1 or self.user_settings.exists(user_id, "challenge_admin"):
            self.user_settings.upsert(user_id, "challenge_admin", "1")
            user_exp += 10000

        level, exp = self._calculate_level(user_exp)
        self.user_settings.upsert(user_id, "level", str(level))
        self.user_settings.upsert(user_id, "experience", str(exp))

        return ChallengeProgress(level, exp, history_count, topic_count)

    def _upsert_history_challenges(self, user_id: str, history_count: int) -> int:
        user_exp = 0

        if history_count >= 1:
            self.user_settings.upsert(user_id, "challenge_first_contribute", "1")
            user_exp += 500

        if history_count >= 10:
            self.user_settings.upsert(user_id, "challenge_tenth_contribute", "1")
            user_exp += 1000

        if history_count >= 100:
            self.user_settings.upsert(user_id, "challenge_hundredth_contribute", "1")
            user_exp += 3000

        if history_count >= 1000:
            self.user_settings.upsert(user_id, "challenge_thousandth_contribute", "1")
            user_exp += 10000

        return user_exp

    def _upsert_topic_challenges(self, user_id: str, topic_count: int) -> int:
        user_exp = 0

        if topic_count >= 1:
            self.user_settings.upsert(user_id, "challenge_first_discussion", "1")
            user_exp += 500

        if topic_count >= 10:
            self.user_settings.upsert(user_id, "challenge_tenth_discussion", "1")
            user_exp += 1000

        if topic_count >= 100:
            self.user_settings.upsert(user_id, "challenge_hundredth_discussion", "1")
            user_exp += 3000

        if topic_count >= 1000:
            self.user_settings.upsert(user_id, "challenge_thousandth_discussion", "1")
            user_exp += 10000

        return user_exp

    def _calculate_level(self, user_exp: int) -> tuple[int, int]:
        exp = user_exp
        level = 0

        while exp >= 500 + level * 50:
            exp -= 500 + level * 50
            level += 1

        return level, exp
