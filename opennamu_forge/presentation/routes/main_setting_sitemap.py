import flask

from opennamu_forge.presentation.authorization_helpers import acl_check
from opennamu_forge.presentation.dependencies import (
    get_other_setting_repository,
    get_wiki_document_repository,
)
from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.response_helpers import (
    get_lang,
    load_domain,
    re_error,
    redirect,
    render_template,
)


async def main_setting_sitemap(do_type = 0):
    if not do_type == 1:
        if await acl_check('', 'owner_auth', '', '') == 1:
            return await re_error(0)

    other_settings = get_other_setting_repository()
    wiki_documents = get_wiki_document_repository()
    
    if do_type == 1 or flask.request.method == 'POST':
        if not do_type == 1:
            await acl_check(tool = 'owner_auth', memo = 'make sitemap')

        data = '' + \
            '<?xml version="1.0" encoding="UTF-8"?>\n' + \
            '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
        ''

        if other_settings.get("sitemap_auto_exclude_domain") != '':
            domain = ''
        else:
            domain = load_domain('full')

        all_data = wiki_documents.list_titles(
            exclude_user_pages=other_settings.get("sitemap_auto_exclude_user_page") != '',
            exclude_file_pages=other_settings.get("sitemap_auto_exclude_file_page") != '',
            exclude_category_pages=other_settings.get("sitemap_auto_exclude_category_page") != '',
        )

        len_all_data = len(all_data)
        count = int(len_all_data / 30000)

        for i in range(count + 1):
            data += '<sitemap><loc>' + domain + '/sitemap_' + str(i) + '.xml</loc></sitemap>\n'

        data += '' + \
            '</sitemapindex>' + \
        ''

        f = open("sitemap.xml", 'w')
        f.write(data)
        f.close()

        for i in range(count + 1):
            data = '' + \
                '<?xml version="1.0" encoding="UTF-8"?>\n' + \
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
            ''

            if count == i:
                for x in all_data[30000 * i:]:
                    data += '<url><loc>' + domain + '/w/' + url_pas(x) + '</loc></url>\n'
            else:
                for x in all_data[30000 * i:30000 * (i + 1)]:
                    data += '<url><loc>' + domain + '/w/' + url_pas(x) + '</loc></url>\n'

            data += '' + \
                '</urlset>' + \
            ''

            f = open("sitemap_" + str(i) + ".xml", 'w')
            f.write(data)
            f.close()

        if not do_type == 1:
            return redirect('/setting/sitemap')
        else:
            return ''
    else:
        return await render_template(
            await get_lang('sitemap_manual_create'),
            '''
                <form method="post">
                    <button class="__ON_BUTTON__" id="opennamu_forge_save_button" type="submit">''' + await get_lang('create') + '''</button>
                </form>
            ''',
            0,
            [['setting/sitemap_set', await get_lang('return')]]
        )
