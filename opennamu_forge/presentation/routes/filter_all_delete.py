from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.shared.func import (
    re_error,
)
from opennamu_forge.presentation.response_helpers import redirect
from opennamu_forge.presentation.dependencies import get_html_filter_repository
async def filter_all_delete(tool, name = 'Test'):
    html_filters = get_html_filter_repository()
    
    if await acl_check(tool = 'owner_auth', memo = 'del_' + tool) == 1:
        return await re_error(3)

    if tool == 'inter_wiki':
        html_filters.delete(name, 'inter_wiki')
        html_filters.delete(name, 'inter_wiki_sub')
    elif tool == 'edit_filter':
        html_filters.delete(name, 'regex_filter')
    elif tool == 'name_filter':
        html_filters.delete(name, 'name')
    elif tool == 'file_filter':
        html_filters.delete(name, 'file')
    elif tool == 'email_filter':
        html_filters.delete(name, 'email')
    elif tool == 'image_license':
        html_filters.delete(name, 'image_license')
    elif tool == 'extension_filter':
        html_filters.delete(name, 'extension')
    elif tool == 'document':
        html_filters.delete(name, 'document')
    elif tool == 'outer_link':
        html_filters.delete(name, 'outer_link')
    elif tool == 'template':
        html_filters.delete(name, 'template')
    else:
        html_filters.delete(name, 'edit_top')

    return redirect('/filter/' + tool)
