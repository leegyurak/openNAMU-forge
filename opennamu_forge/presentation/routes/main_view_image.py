from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.file_helpers import load_image_url
from opennamu_forge.presentation.shared.func import (
    flask,
    re,
    re_error,
)

async def main_view_image(name = ''):
    if await acl_check('', 'render') != 1:
        name = re.sub(r'\.cache_v(?:[0-9]+)$', '', name)
        mime_type = re.search(r'([^.]+)$', name)
        if mime_type:
            mime_type = mime_type.group(1).lower()
            if mime_type == 'svg':
                mime_type = 'svg+xml'

            return flask.send_from_directory('./' + load_image_url(), name, mimetype = 'image/' + mime_type)
        else:
            return ''
    else:
        return await re_error(0)