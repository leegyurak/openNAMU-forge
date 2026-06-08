from types import SimpleNamespace

import flask


def test_app_import는_runtime을_로드하지_않는다():
    import app

    assert app._runtime_app_module is None


def test_create_app은_호출시에만_runtime_app을_로드한다(monkeypatch):
    import app

    fake_flask_app = flask.Flask(__name__)
    fake_runtime_module = SimpleNamespace(app=fake_flask_app)
    app._runtime_app_module = None

    def fake_import_module(module_name):
        assert module_name == "opennamu_forge.presentation.runtime_app"
        return fake_runtime_module

    monkeypatch.setattr(app.importlib, "import_module", fake_import_module)

    assert app.create_app() is fake_flask_app
    assert app.load_runtime_app() is fake_runtime_module

    app._runtime_app_module = None
