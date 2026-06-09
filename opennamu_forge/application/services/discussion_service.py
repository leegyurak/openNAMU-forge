from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol

from opennamu_forge.application.ports.notifications import AlarmPort


class DiscussionTopicStore(Protocol):
    def latest_comment_id(self, code: str) -> int | None: ...
    def add_comment(self, code: str, comment_id: str, data: str, date: str, ip: str, block: str, *, top: str = "") -> None: ...
    def update_recent_discuss_date(self, code: str, date: str) -> bool: ...
    def add_recent_discuss(self, code: str, title: str, subtitle: str, date: str) -> None: ...


@dataclass(frozen=True)
class DiscussionService:
    topics: DiscussionTopicStore
    alarms: AlarmPort
    now_provider: Callable[[], str]
    actor_provider: Callable[[], str]

    def add_thread_comment(self, thread_code: str, thread_data: str, thread_top: str = "", thread_id: str = "") -> None:
        if thread_id == "":
            latest_comment_id = self.topics.latest_comment_id(thread_code)
            thread_id = str(latest_comment_id + 1) if latest_comment_id is not None else "1"

        self.topics.add_comment(
            thread_code,
            thread_id,
            thread_data,
            self.now_provider(),
            self.actor_provider(),
            thread_top,
        )

    def reload_recent_thread(self, topic_num: str, date: str, name: str = "", sub: str = "") -> None:
        if not self.topics.update_recent_discuss_date(topic_num, date):
            self.topics.add_recent_discuss(topic_num, name, sub, date)

    async def add_alarm(self, to_user: str, from_user: str, context: str) -> None:
        await self.alarms.send_alarm(to_user, from_user, context)
