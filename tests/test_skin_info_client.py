from opennamu_forge.infrastructure.skin_info_client import SkinInfoClient


class FakeResponse:
    def __init__(self, code, body):
        self._code = code
        self._body = body

    def getcode(self):
        return self._code

    def read(self):
        return self._body


def test_skin_info_client는_skin_ver를_dto로_반환한다():
    client = SkinInfoClient(lambda info_link: FakeResponse(200, b'{"skin_ver": "1.2.3"}'))

    latest_info = client.fetch_latest_info("https://example.com/info.json")

    assert latest_info is not None
    assert latest_info.skin_ver == "1.2.3"


def test_skin_info_client는_200이_아니면_none을_반환한다():
    client = SkinInfoClient(lambda info_link: FakeResponse(404, b'{"skin_ver": "1.2.3"}'))

    assert client.fetch_latest_info("https://example.com/info.json") is None


def test_skin_info_client는_json이_아니면_none을_반환한다():
    client = SkinInfoClient(lambda info_link: FakeResponse(200, b"not-json"))

    assert client.fetch_latest_info("https://example.com/info.json") is None


def test_skin_info_client는_skin_ver가_없으면_none을_반환한다():
    client = SkinInfoClient(lambda info_link: FakeResponse(200, b'{"name": "Ringo"}'))

    assert client.fetch_latest_info("https://example.com/info.json") is None


def test_skin_info_client는_network_error면_none을_반환한다():
    def fake_urlopen(info_link):
        raise OSError

    client = SkinInfoClient(fake_urlopen)

    assert client.fetch_latest_info("https://example.com/info.json") is None
