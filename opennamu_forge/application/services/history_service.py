from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Protocol


class HistoryMutationHistory(Protocol):
    def count_recent_changes_by_type(self, change_type: str) -> int: ...
    def oldest_recent_change_ref_by_type(self, change_type: str) -> tuple[str, str] | None: ...
    def delete_recent_change(self, title: str, revision_id: str, change_type: str) -> None: ...
    def earliest_revision_id(self, title: str) -> str | None: ...
    def latest_revision_id(self, title: str) -> str | None: ...
    def add_recent_change(self, title: str, revision_id: str, date: str, change_type: str) -> None: ...
    def add_history(
        self,
        title: str,
        revision_id: str,
        data: str,
        date: str,
        ip: str,
        send: str,
        length: str,
        change_type: str,
    ) -> None: ...


class HistoryMutationDocumentMeta(Protocol):
    def delete(self, doc_name: str, set_name: str, *, doc_rev: str = "") -> None: ...
    def upsert(self, doc_name: str, set_name: str, set_data: str, *, doc_rev: str = "") -> None: ...
    def update_revision_marker(self, doc_name: str, doc_rev: str) -> None: ...


class HistoryMutationOtherSettings(Protocol):
    def get(self, name: str, *, coverage: str = "", default: str = "") -> str: ...
    def upsert(self, name: str, data: str, *, coverage: str = "") -> None: ...


class HistoryMutationWikiDocuments(Protocol):
    def count_all_titles(self) -> int: ...


@dataclass(frozen=True)
class HistoryMutationService:
    history: HistoryMutationHistory
    document_meta: HistoryMutationDocumentMeta
    other_settings: HistoryMutationOtherSettings
    wiki_documents: HistoryMutationWikiDocuments

    def enforce_recent_change_limit(self, mode: str) -> None:
        if self.history.count_recent_changes_by_type(mode) >= 200:
            rc_data = self.history.oldest_recent_change_ref_by_type(mode)
            if rc_data:
                self.history.delete_recent_change(rc_data[1], rc_data[0], mode)

    def add_history(
        self,
        title: str,
        data: str,
        date: str,
        ip: str,
        send: str,
        length: str,
        t_check: str = "",
        mode: str = "",
    ) -> int | None:
        if self.other_settings.get("history_recording_off") != "":
            return 0

        if mode in {"add", "setting"}:
            id_data = self.history.earliest_revision_id(title)
            id_data = str(int(id_data) - 1) if id_data else "0"
        else:
            id_data = self.history.latest_revision_id(title)
            id_data = str(int(id_data) + 1) if id_data else "1"

            mode = "r1" if id_data == "1" else mode
            if re.search("^user:", title):
                mode = "user"
            elif re.search("^file:", title):
                mode = "file"
            elif re.search("^category:", title):
                mode = "category"

        send = re.sub(r"<|>", "", send)
        send = send[:512] if len(send) > 512 else send
        send = send + " (" + t_check + ")" if t_check != "" else send

        if mode not in {"add", "setting", "user"}:
            self.enforce_recent_change_limit("normal")
            self.history.add_recent_change(title, id_data, date, "normal")

        if mode not in {"add", "setting"}:
            self.enforce_recent_change_limit(mode)

            count_data = self.wiki_documents.count_all_titles()
            self.other_settings.upsert("count_all_title", str(count_data))

            self.history.add_recent_change(title, id_data, date, mode)

            data_set_exist = "not_exist" if mode == "delete" else ""

            self.document_meta.delete(title, "edit_request_doing")
            self.document_meta.upsert(title, "last_edit", date)
            self.document_meta.upsert(title, "length", str(len(data)))
            self.document_meta.update_revision_marker(title, data_set_exist)

        self.history.add_history(title, id_data, data, date, ip, send, length, mode)
        return None
