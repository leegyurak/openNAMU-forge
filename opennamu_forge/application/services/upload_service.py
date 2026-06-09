from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UploadPolicyService:
    def normalize_content_length(self, content_length: int | None) -> int:
        return 0 if content_length is None else content_length

    def is_size_invalid(self, max_file_mb: int, file_count: int, content_length: int) -> bool:
        return (max_file_mb * 1000 * 1000 * file_count) < content_length or content_length == 0

    def initial_file_number(self, file_count: int, *, can_many_upload: bool) -> int | None:
        if file_count == 1:
            return None

        if can_many_upload:
            return 1

        return 0

    def build_upload_title(self, original_name: str, requested_name: str, file_number: int | None, extension: str) -> str:
        if requested_name != "":
            suffix = " " + str(file_number) if file_number else ""
            return requested_name + suffix + extension

        return original_name

    def build_file_document_text(self, markup: str, license_selection: str, license_text: str) -> str:
        if markup == "namumark":
            return license_selection + "\n" + "[[category:" + license_selection.replace("]", "_") + "]]\n" + license_text

        return license_selection + "\n" + license_text
