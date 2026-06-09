from flask import Flask
from werkzeug.routing import Map

from opennamu_forge.presentation.url_converters import EverythingConverter, RegexConverter, register_url_converters


def test_everything_converter는_escaped_dot을_원래_dot으로_복원한다():
    converter = EverythingConverter(Map())

    assert converter.to_python(r"\.hidden/page") == ".hidden/page"


def test_regex_converter는_전달된_regex를_저장한다():
    converter = RegexConverter(Map(), r"[a-z]+")

    assert converter.regex == r"[a-z]+"


def test_register_url_converters는_flask_app에_converter를_등록한다():
    app = Flask(__name__)

    register_url_converters(app)

    assert app.url_map.converters["everything"] is EverythingConverter
    assert app.url_map.converters["regex"] is RegexConverter
