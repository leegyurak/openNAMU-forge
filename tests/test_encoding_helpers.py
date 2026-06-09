from opennamu_forge.presentation import encoding_helpers


def test_url_pas는_기존_url_escape_동작을_유지한다():
    assert encoding_helpers.url_pas("./A/B") == "%5C.%2FA%2FB"


def test_sha224_replace는_기존_hash_동작을_유지한다():
    assert encoding_helpers.sha224_replace("OpenNamu Forge") == "a80cdeda8410c42f471fe2eafa4c1fc66ab84a2634522591f4b74f2f"


def test_md5_replace는_기존_hash_동작을_유지한다():
    assert encoding_helpers.md5_replace("OpenNamu Forge") == "741c396b18a6f4d87f84c382dcbe9a10"


def test_json_helpers는_문자열_round_trip을_유지한다():
    payload = {"project": "opennamu-forge", "count": 1}

    encoded = encoding_helpers.json_dumps(payload)

    assert isinstance(encoded, str)
    assert encoding_helpers.json_loads(encoded) == payload
