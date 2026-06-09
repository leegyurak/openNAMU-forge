from __future__ import annotations

from typing import Any, cast

import flask

from opennamu_forge.application.runtime_context import get_runtime_value
from opennamu_forge.presentation.encoding_helpers import md5_replace, url_pas
from opennamu_forge.presentation.response_helpers import load_lang
from opennamu_forge.presentation.text_helpers import cut_100


def register_wiki_access_gate(app: flask.Flask) -> None:
    @app.before_request
    def before_request_func() -> str | None:
        db_data = get_runtime_value("wiki_access_password")
        if db_data and db_data != "":
            access_password = db_data
            input_password = flask.request.cookies.get("opennamu_forge_wiki_access", " ")
            if url_pas(access_password) != input_password:
                return '''
                <script>
                    "use strict";
                    function opennamu_forge_do_wiki_access() {
                        let password = document.getElementById('wiki_access').value;
                        document.cookie = 'opennamu_forge_wiki_access=' + encodeURIComponent(password) + '; path=/;';
                        history.go(0);
                    }
                </script>
                <h2>''' + load_lang("error_password_require_for_wiki_access") + '''</h2>
                <input class="__ON_INPUT__" type="password" id="wiki_access">
                <input class="__ON_INPUT__" type="submit" onclick="opennamu_forge_do_wiki_access();">
            '''

        return None


def register_template_filters(app: flask.Flask) -> None:
    app.jinja_env.filters["md5_replace"] = md5_replace
    app.jinja_env.filters["load_lang"] = load_lang
    app.jinja_env.filters["cut_100"] = cut_100


def enable_dev_template_reload(app: flask.Flask) -> None:
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

    app.jinja_options["cache_size"] = 0
    app.jinja_options["auto_reload"] = True
    app.jinja_options["bytecode_cache"] = None


def apply_proxy_fix(app: flask.Flask) -> None:
    from werkzeug.middleware.proxy_fix import ProxyFix

    app.wsgi_app = cast(Any, ProxyFix(app.wsgi_app, x_for=1, x_proto=1))
