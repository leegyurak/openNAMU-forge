from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.file_helpers import load_image_url
from opennamu_forge.presentation.encoding_helpers import (
    sha224_replace,
    url_pas,
)
from opennamu_forge.presentation.shared.func import (
    flask,
    os,
    re,
    re_error,
)
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    redirect,
    render_template,
)
from .edit_delete import edit_delete

async def edit_delete_file(name = 'test.jpg'):
    if await acl_check('', 'owner_auth', '', '') != 0:
        return await re_error(0)

    mime_type = re.search(r'([^.]+)$', name)
    mime_type_str = 'jpg'
    if mime_type:
        mime_type_str = mime_type.group(1)

    file_name = re.sub(r'\.([^.]+)$', '', name)
    file_name = re.sub(r'^file:', '', file_name)

    file_all_name = sha224_replace(file_name) + '.' + mime_type_str
    file_directory = os.path.join(load_image_url(), file_all_name)

    if not os.path.exists(file_directory):
        return redirect('/w/' + url_pas(name))

    if flask.request.method == 'POST':
        await acl_check(tool = 'owner_auth', memo = 'file del (' + name + ')')
        os.remove(file_directory)

        if flask.request.form.get('with_doc', '') != '':
            await edit_delete(name)

        return redirect('/w/' + url_pas(name))
    else:
        return await render_template(
            name,
            '''
                <form method="post">
                    <img src="/image/''' + url_pas(file_all_name) + '''">
                    <hr class="main_hr">
                    <a href="/image/''' + url_pas(file_all_name) + '''">/image/''' + url_pas(file_all_name) + '''</a>
                    <hr class="main_hr">
                    <label class="__ON_CHECKLABEL__"><input class="__ON_CHECKBOX__" name="with_doc" type="checkbox" checked> ''' + await get_lang('file_delete_with_document') + '''</label>
                    <hr class="main_hr">
                    <button class="__ON_BUTTON__" type="submit">''' + await get_lang('file_delete') + '''</button>
                </form>
            ''',
            '(' + await get_lang('file_delete') + ')',
            [['w/' + url_pas(name), await get_lang('return')]]
        )
