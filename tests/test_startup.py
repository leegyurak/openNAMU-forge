from dataclasses import FrozenInstanceError

import pytest

from opennamu_forge.application.startup import RuntimeSettings, normalize_run_mode


def test_run_mode는_dev만_허용한다():
    assert normalize_run_mode("dev") == "dev"
    assert normalize_run_mode("prod") == ""
    assert normalize_run_mode("DEV") == ""
    assert normalize_run_mode("") == ""


def test_runtime_settings는_불변이다():
    settings = RuntimeSettings(run_mode="dev", host="0.0.0.0", port="3000", golang_port="3001")

    assert settings.run_mode == "dev"
    assert settings.host == "0.0.0.0"

    with pytest.raises(FrozenInstanceError):
        setattr(settings, "run_mode", "")
