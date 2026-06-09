from opennamu_forge.application.runtime_context import clear_runtime_context, get_runtime_value, set_runtime_value


def test_runtime_state는_없는_key에서_none을_반환한다():
    clear_runtime_context()

    assert get_runtime_value("missing") is None


def test_runtime_state는_값을_저장하고_조회한다():
    clear_runtime_context()

    assert set_runtime_value("NAMU_DB", "wiki") == "wiki"
    assert get_runtime_value("NAMU_DB") == "wiki"
