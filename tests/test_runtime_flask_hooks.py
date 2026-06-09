import flask

from opennamu_forge.application.runtime_context import clear_runtime_context, set_runtime_value
from opennamu_forge.presentation.encoding_helpers import md5_replace
from opennamu_forge.presentation.response_helpers import load_lang
from opennamu_forge.presentation.runtime.flask_hooks import (
    enable_dev_template_reload,
    register_template_filters,
    register_wiki_access_gate,
)
from opennamu_forge.presentation.text_helpers import cut_100


def test_wiki_access_gate는_password가_없으면_request를_통과시킨다():
    clear_runtime_context()
    app = flask.Flask(__name__)
    register_wiki_access_gate(app)

    @app.get("/")
    def index():
        return "ok"

    response = app.test_client().get("/")

    assert response.data == b"ok"
    clear_runtime_context()


def test_wiki_access_gate는_password가_있으면_gate_html을_반환한다(monkeypatch):
    clear_runtime_context()
    set_runtime_value("wiki_access_password", "secret")
    monkeypatch.setattr("opennamu_forge.presentation.runtime.flask_hooks.load_lang", lambda data: data)
    app = flask.Flask(__name__)
    register_wiki_access_gate(app)

    @app.get("/")
    def index():
        return "ok"

    response = app.test_client().get("/")

    assert response.status_code == 200
    assert b"wiki_access" in response.data
    clear_runtime_context()


def test_runtime_flask_hooks는_template_filter와_dev_reload를_설정한다():
    app = flask.Flask(__name__)

    register_template_filters(app)
    enable_dev_template_reload(app)

    assert app.jinja_env.filters["md5_replace"] is md5_replace
    assert app.jinja_env.filters["load_lang"] is load_lang
    assert app.jinja_env.filters["cut_100"] is cut_100
    assert app.config["TEMPLATES_AUTO_RELOAD"] is True
    assert app.jinja_options["auto_reload"] is True
