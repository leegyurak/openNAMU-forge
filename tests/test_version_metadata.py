from opennamu_forge.application.version import VERSION_INFO


def test_version_metadata는_runtime_필수_key를_제공한다():
    assert VERSION_INFO["r_ver"].startswith("v")
    assert VERSION_INFO["c_ver"].isdigit()
    assert VERSION_INFO["s_ver"].isdigit()
    assert VERSION_INFO["bin_link"].startswith("https://")
