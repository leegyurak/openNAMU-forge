from __future__ import annotations

from pathlib import Path
from collections.abc import Iterable
from typing import Protocol

import requests


class StreamingResponse(Protocol):
    status_code: int

    def iter_content(self, chunk_size: int) -> Iterable[bytes]:
        pass


def download_binary(
    download_url: str,
    local_file_path: Path,
    *,
    get_response=requests.get,
    chunk_size: int = 8192,
) -> bool:
    response: StreamingResponse = get_response(download_url, stream=True)
    if response.status_code != 200:
        return False

    with local_file_path.open("wb") as file:
        for chunk in response.iter_content(chunk_size=chunk_size):
            file.write(chunk)

    return True


def ensure_gopennamu_binary(
    *,
    run_mode: str,
    setup_tool: str,
    bin_dir: str,
    version_list: dict[str, str],
    executable_name: str,
    logger,
    get_response=requests.get,
) -> None:
    if run_mode == "dev":
        return

    local_file_path = Path(bin_dir) / executable_name
    if setup_tool == "normal" and local_file_path.exists():
        return

    if local_file_path.exists():
        logger.info("Remove Old Binary")
        local_file_path.unlink()

    logger.info("Download New Binary File")
    downloaded = download_binary(
        version_list["bin_link"] + executable_name,
        local_file_path,
        get_response=get_response,
    )
    if downloaded:
        logger.info("Complete Download")
