from opennamu_forge.presentation.route_registry import register_routes


class FakeApp:
    def __init__(self):
        self.routes = []
        self.get_routes = []
        self.error_handlers = []

    def route(self, rule, **options):
        self.routes.append((rule, options))

        def decorator(view_func):
            return view_func

        return decorator

    def get(self, rule, **options):
        self.get_routes.append((rule, options))

        def decorator(view_func):
            return view_func

        return decorator

    def errorhandler(self, code):
        self.error_handlers.append(code)

        def decorator(view_func):
            return view_func

        return decorator


def test_route_registry는_주요_route와_errorhandler를_등록한다():
    app = FakeApp()
    process = object()

    register_routes(app, version_list={"r_ver": "test"}, golang_process=process)

    assert ("/filter/inter_wiki", {"defaults": {"tool": "inter_wiki"}}) in app.routes
    assert ("/api/version", {"defaults": {"version_list": {"r_ver": "test"}}}) in app.routes
    assert ("/restart", {"defaults": {"golang_process": process}, "methods": ["POST", "GET"]}) in app.routes
    assert app.get_routes == [("/forge/theme.css.cache_v1", {})]
    assert app.error_handlers == [404]
