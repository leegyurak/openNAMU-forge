from opennamu_forge.presentation.encoding_helpers import url_pas
from opennamu_forge.presentation.shared.func import render_set
from opennamu_forge.presentation.response_helpers import redirect
from opennamu_forge.presentation.dependencies import get_wiki_document_repository
async def edit_backlink_reset(name = 'Test'):
    wiki_documents = get_wiki_document_repository()

    if wiki_documents.exists_title(name):
        old = wiki_documents.get_data(name)
        await render_set(
            doc_name = name,
            doc_data = old,
            data_type = 'backlink'
        )

    return redirect('/xref/' + url_pas(name))
