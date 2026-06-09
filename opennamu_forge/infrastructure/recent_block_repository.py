from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from sqlalchemy import func, update
from sqlmodel import col, select

from opennamu_forge.infrastructure.db_model import RecentBlock, get_sqlmodel_session


@dataclass(frozen=True)
class RecentBlockRepository:
    db_set: dict[str, str]

    def get_ongoing_end(self, block: str, *, default: str = "") -> str:
        with get_sqlmodel_session(self.db_set) as session:
            value = select(RecentBlock.end).where(RecentBlock.block == block, RecentBlock.ongoing == "1").limit(1)

            return cast(str, session.exec(select(func.coalesce(value.scalar_subquery(), default))).one())

    def close_ongoing(self, block: str, band: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(
                update(RecentBlock)
                .where(
                    col(RecentBlock.block) == block,
                    col(RecentBlock.band) == band,
                    col(RecentBlock.ongoing) == "1",
                )
                .values(ongoing="")
            )
            session.commit()

    def close_expired(self, now: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.exec(
                update(RecentBlock)
                .where(col(RecentBlock.end) < now, col(RecentBlock.end) != "", col(RecentBlock.ongoing) == "1")
                .values(ongoing="")
            )
            session.commit()

    def add_record(self, block: str, end: str, today: str, blocker: str, why: str, band: str, ongoing: str, login: str) -> None:
        with get_sqlmodel_session(self.db_set) as session:
            session.add(RecentBlock(block=block, end=end, today=today, blocker=blocker, why=why, band=band, ongoing=ongoing, login=login))
            session.commit()
