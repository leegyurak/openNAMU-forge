from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TopicCommentDTO:
    code: str
    comment_id: str
    data: str
    date: str
    author: str
    block: str
    top: str


@dataclass(frozen=True)
class RecentDiscussDTO:
    title: str
    subtitle: str
    code: str
    stop: str
    agree: str
    acl: str
