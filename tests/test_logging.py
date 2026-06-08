from opennamu_forge.infrastructure.logging import configure_logging, get_logger


def test_logger는_환경변수_레벨을_사용한다(monkeypatch):
    monkeypatch.setenv("NAMU_LOG_LEVEL", "WARNING")

    configure_logging()
    logger = get_logger("opennamu_forge.test")

    assert logger.name == "opennamu_forge.test"
