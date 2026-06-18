from pathlib import Path

import pytest

from opennamu_forge.presentation.runtime.gopennamu_binary import (
    download_binary,
    ensure_gopennamu_binary,
)


class FakeLogger:
    def __init__(self):
        self.messages = []

    def info(self, message):
        self.messages.append(message)


class FakeResponse:
    def __init__(self, status_code=200, chunks=(b"binary",)):
        self.status_code = status_code
        self.chunks = chunks
        self.chunk_sizes = []

    def iter_content(self, chunk_size):
        self.chunk_sizes.append(chunk_size)
        return self.chunks


def test_download_binary는_200_응답을_파일로_저장한다(tmp_path):
    response = FakeResponse(chunks=(b"go", b"namu"))
    calls = []

    def fake_get_response(download_url, stream):
        calls.append((download_url, stream))
        return response

    local_file_path = tmp_path / "main.bin"

    downloaded = download_binary(
        "https://example.test/main.bin",
        local_file_path,
        get_response=fake_get_response,
    )

    assert downloaded is True
    assert calls == [("https://example.test/main.bin", True)]
    assert response.chunk_sizes == [8192]
    assert local_file_path.read_bytes() == b"gonamu"


def test_download_binary는_실패_응답이면_파일을_만들지_않는다(tmp_path):
    local_file_path = tmp_path / "main.bin"

    downloaded = download_binary(
        "https://example.test/main.bin",
        local_file_path,
        get_response=lambda download_url, stream: FakeResponse(status_code=404),
    )

    assert downloaded is False
    assert not local_file_path.exists()


@pytest.mark.parametrize(
    ("run_mode", "setup_tool", "existing_data", "expected_data", "expected_calls"),
    [
        ("dev", "update", b"old", b"old", []),
        ("dev", "update", None, b"new", ["https://example.test/main.bin"]),
        ("", "normal", b"old", b"old", []),
        ("", "update", b"old", b"new", ["https://example.test/main.bin"]),
        ("", "init", None, b"new", ["https://example.test/main.bin"]),
    ],
)
def test_ensure_gopennamu_binary는_필요할_때만_다운로드한다(
    tmp_path,
    run_mode,
    setup_tool,
    existing_data,
    expected_data,
    expected_calls,
):
    local_file_path = Path(tmp_path) / "main.bin"
    if existing_data is not None:
        local_file_path.write_bytes(existing_data)
    calls = []

    def fake_get_response(download_url, stream):
        calls.append(download_url)
        return FakeResponse(chunks=(b"new",))

    ensure_gopennamu_binary(
        run_mode=run_mode,
        setup_tool=setup_tool,
        bin_dir=str(tmp_path),
        version_list={"bin_link": "https://example.test/"},
        executable_name="main.bin",
        logger=FakeLogger(),
        get_response=fake_get_response,
    )

    assert calls == expected_calls
    assert local_file_path.read_bytes() == expected_data
