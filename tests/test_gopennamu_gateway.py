import pytest
from flask import Flask

from opennamu_forge.application.runtime_context import clear_runtime_context, set_runtime_value
from opennamu_forge.presentation import gopennamu_gateway


def test_gopennamu_gateway는_flask_context가_없으면_empty_context를_만든다():
    context = gopennamu_gateway.build_gopennamu_request_context()

    assert context.method == "GET"
    assert context.path == ""
    assert context.headers == {}
    assert context.form_data is None


def test_gopennamu_gateway는_flask_request를_context로_변환한다(monkeypatch):
    monkeypatch.setattr(gopennamu_gateway, "ip_check", lambda: "127.0.0.2")
    app = Flask(__name__)

    with app.test_request_context("/w/Test", method="POST", headers={"Cookie": "sid=1"}, data={"name": "Test"}):
        context = gopennamu_gateway.build_gopennamu_request_context()

    assert context.method == "POST"
    assert context.path == "/w/Test"
    assert context.headers == {"X-Forwarded-For": "127.0.0.2", "Cookie": "sid=1"}
    assert context.form_data == {"name": ["Test"]}


def test_gopennamu_gateway는_runtime_port로_client를_생성한다():
    clear_runtime_context()
    set_runtime_value("setup_golang_port", "3301")

    client = gopennamu_gateway.build_gopennamu_client()

    assert client.base_url == "http://127.0.0.1:3301"


def test_gopennamu_gateway는_runtime_port가_없으면_예외를_낸다():
    clear_runtime_context()

    with pytest.raises(RuntimeError, match="GopenNAMU port"):
        gopennamu_gateway.build_gopennamu_client()
