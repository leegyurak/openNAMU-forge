from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from opennamu_forge.application.dto.history import HistoryRecordDTO


class RecentChangeHistoryStore(Protocol):
    def list_records_by_title(self, title: str, *, offset: int = 0, limit: int = 50) -> list[HistoryRecordDTO]: ...
    def list_records_by_title_type(
        self, title: str, change_type: str, *, offset: int = 0, limit: int = 50
    ) -> list[HistoryRecordDTO]: ...
    def list_records_by_ip(self, ip: str, *, offset: int = 0, limit: int = 50) -> list[HistoryRecordDTO]: ...
    def list_records_by_ip_type(self, ip: str, change_type: str, *, offset: int = 0, limit: int = 50) -> list[HistoryRecordDTO]: ...
    def list_recent_change_records_by_type(self, change_type: str, *, limit: int = 50) -> list[HistoryRecordDTO]: ...
    def list_records_by_type(self, change_type: str, *, offset: int = 0, limit: int = 50) -> list[HistoryRecordDTO]: ...
    def list_records(self, *, offset: int = 0, limit: int = 50) -> list[HistoryRecordDTO]: ...


@dataclass(frozen=True)
class RecentChangeQueryResult:
    records: list[HistoryRecordDTO]
    normalized_set_type: str


@dataclass(frozen=True)
class RecentChangeService:
    history: RecentChangeHistoryStore

    def list_records(self, name: str, tool: str, num: int, set_type: str, *, can_page_all: bool) -> RecentChangeQueryResult:
        offset = num * 50 - 50 if num * 50 > 0 else 0

        normalized_set_type = "" if set_type == "edit" else set_type
        if tool == "history":
            return RecentChangeQueryResult(
                self._list_history_records(name, normalized_set_type, offset),
                normalized_set_type,
            )

        if tool == "record":
            return RecentChangeQueryResult(
                self._list_record_records(name, normalized_set_type, offset),
                normalized_set_type,
            )

        return RecentChangeQueryResult(
            self._list_recent_records(num, normalized_set_type, offset, can_page_all=can_page_all),
            normalized_set_type,
        )

    def _list_history_records(self, name: str, set_type: str, offset: int) -> list[HistoryRecordDTO]:
        if set_type != "normal":
            return self.history.list_records_by_title_type(name, set_type, offset=offset)

        return self.history.list_records_by_title(name, offset=offset)

    def _list_record_records(self, name: str, set_type: str, offset: int) -> list[HistoryRecordDTO]:
        if set_type != "normal":
            return self.history.list_records_by_ip_type(name, set_type, offset=offset)

        return self.history.list_records_by_ip(name, offset=offset)

    def _list_recent_records(self, num: int, set_type: str, offset: int, *, can_page_all: bool) -> list[HistoryRecordDTO]:
        if num == 1 or not can_page_all:
            return self.history.list_recent_change_records_by_type(set_type)

        if set_type != "normal":
            return self.history.list_records_by_type(set_type, offset=offset)

        return self.history.list_records(offset=offset)
