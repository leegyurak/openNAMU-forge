from opennamu_forge.application.services.version_service import build_version_payload


class FakeSettings:
    def get(self, name, *, coverage="", default=""):
        assert name != "update"
        assert coverage == ""
        assert default == ""
        return ""


def test_version_payload는_forge_build를_반환한다():
    payload = build_version_payload(
        {"r_ver": "v1", "c_ver": "2", "s_ver": "3"},
        FakeSettings(),
    )

    assert payload == {
        "version": "v1",
        "db_version": "2",
        "skin_version": "3",
        "build": "forge",
    }
