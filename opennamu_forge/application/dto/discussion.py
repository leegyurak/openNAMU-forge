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
