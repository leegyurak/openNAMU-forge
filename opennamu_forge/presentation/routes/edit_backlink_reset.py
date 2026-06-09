from .tool.func import *

async def edit_backlink_reset(name = 'Test'):
    with get_db_connect() as conn:
        wiki_documents = get_wiki_document_repository()

        if wiki_documents.exists_title(name):
            old = wiki_documents.get_data(name)
            await render_set(conn, 
                doc_name = name,
                doc_data = old,
                data_type = 'backlink'
            )

        return redirect(conn, '/xref/' + url_pas(name))
