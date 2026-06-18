import asyncio

from opennamu_forge.presentation.flask_factory import create_flask_app
from opennamu_forge.presentation.routes.main_view import main_view


def test_main_view는_cache_suffix_css를_project_views에서_serving한다():
    app = create_flask_app(base_dir=".", run_mode="dev", version="test", db_type="sqlite")

    with app.test_request_context("/views/main_css/css/main.css.cache_v288"):
        response = asyncio.run(main_view("main_css/css/main.css.cache_v288"))

    assert response.status_code == 200
    assert response.content_type == "text/css; charset=utf-8"
    assert int(response.headers["Content-Length"]) > 0


def test_main_view는_project_views_image를_binary_mimetype으로_serving한다():
    app = create_flask_app(base_dir=".", run_mode="dev", version="test", db_type="sqlite")

    with app.test_request_context("/views/main_css/file/s_logo.webp"):
        response = asyncio.run(main_view("main_css/file/s_logo.webp"))

    assert response.status_code == 200
    assert response.content_type == "image/webp"
    assert int(response.headers["Content-Length"]) > 0


def test_main_view는_ringo_react_css_bundle을_static으로_serving한다():
    app = create_flask_app(base_dir=".", run_mode="dev", version="test", db_type="sqlite")

    with app.test_request_context("/views/ringo/dist/assets/main.css.cache_v1"):
        response = asyncio.run(main_view("ringo/dist/assets/main.css.cache_v1"))

    assert response.status_code == 200
    assert response.content_type == "text/css; charset=utf-8"
    assert int(response.headers["Content-Length"]) > 0


def test_main_view는_ringo_runtime_overrides_css를_static으로_serving한다():
    app = create_flask_app(base_dir=".", run_mode="dev", version="test", db_type="sqlite")

    with app.test_request_context("/views/ringo/dist/assets/runtime-overrides.css.cache_v1"):
        response = asyncio.run(main_view("ringo/dist/assets/runtime-overrides.css.cache_v1"))

    assert response.status_code == 200
    assert response.content_type == "text/css; charset=utf-8"
    assert int(response.headers["Content-Length"]) > 0


def test_main_view는_ringo_react_js_bundle을_static으로_serving한다():
    app = create_flask_app(base_dir=".", run_mode="dev", version="test", db_type="sqlite")

    with app.test_request_context("/views/ringo/dist/assets/main.js.cache_v1"):
        response = asyncio.run(main_view("ringo/dist/assets/main.js.cache_v1"))

    assert response.status_code == 200
    assert response.content_type == "text/javascript; charset=utf-8"
    assert int(response.headers["Content-Length"]) > 0
