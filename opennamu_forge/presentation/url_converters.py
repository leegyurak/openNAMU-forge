import re

import werkzeug.routing


class EverythingConverter(werkzeug.routing.PathConverter):
    regex = r".*?"

    def to_python(self, value):
        return re.sub(r"^\\\.", ".", value)

class RegexConverter(werkzeug.routing.BaseConverter):
    def __init__(self, url_map, *items):
        super().__init__(url_map)
        self.regex = items[0]

def register_url_converters(app):
    app.url_map.converters["everything"] = EverythingConverter
    app.url_map.converters["regex"] = RegexConverter
