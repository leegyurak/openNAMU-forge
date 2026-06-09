from .func_tool import *
from .func_tool import _get_current_db_set

from .func_render_namumark import class_do_render_namumark
from opennamu_forge.infrastructure.backlink_repository import BacklinkRepository
from opennamu_forge.infrastructure.document_meta_repository import DocumentMetaRepository
from opennamu_forge.infrastructure.setting_repository import OtherSettingRepository

# 커스텀 마크 언젠간 다시 추가 예정

class class_do_render:
    def __init__(self, conn, lang_data = {}, markup = '', parameter = {}, parent = None):
        self.conn = conn

        if lang_data == '{}':
            lang_data = {
                'toc' : 'toc',
                'category' : 'category'
            }

        self.lang_data = lang_data
        self.markup = markup
        self.parameter = parameter
        self.parent = parent

    def generate_random_string(self, length = 32):
        characters = string.ascii_letters + string.digits

        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string

    async def do_render(self, doc_name, doc_data, data_type):
        backlinks = BacklinkRepository(_get_current_db_set())
        document_meta = DocumentMetaRepository(_get_current_db_set())
        other_settings = OtherSettingRepository(_get_current_db_set())

        doc_set = {}
        if data_type == 'from':
            doc_set['doc_from'] = 'O'
            data_type = 'view'
        else:
            doc_set['doc_from'] = ''

        if data_type == 'backlink':
            doc_set['doc_type'] = 'view'
        else:
            doc_set['doc_type'] = data_type
        
        doc_set['doc_include'] = self.generate_random_string() + '_'
    
        rep_data = self.markup
        if rep_data == '' and doc_name != '':
            db_data = document_meta.get(doc_name, 'document_markup')
            if db_data != '' and db_data != 'normal':
                rep_data = db_data

        if rep_data == '':
            rep_data = other_settings.get('markup', default='namumark')

        if rep_data == 'namumark' or rep_data == 'namumark_beta':
            data_end = await class_do_render_namumark(
                self.conn,
                doc_name,
                doc_data,
                doc_set,
                self.lang_data,
                parameter = self.parameter,
                parent = self.parent
            )()
        elif rep_data == 'raw':
            data_end = [html.escape(doc_data).replace('\n', '<br>'), '', {}]
        else:
            data_end = [doc_data, '', {}]

        if data_type == 'thread':
            def do_thread_a_change(match):
                data = match[2].replace('#', '')
                data_split = data.split('-')
                if match[1] == 'topic_a' or len(data_split) == 1:
                    return '<a href="' + match[2] + '">' + match[2] + '</a>'
                elif match[1] == 'topic_a_post' and len(data_split) == 3:
                    return '<a href="/bbs/w/' + data_split[2] + '/' + data_split[1] + '#' + data_split[0] + '">#' + data_split[0] + '-' + data_split[1] + '</a>'
                elif len(data_split) == 2:
                    return '<a href="/thread/' + data_split[1] + '#' + data_split[0] + '">' + match[2] + '</a>'
                else:
                    return ''

            data_end[0] = re.sub(r'&lt;(topic_a(?:_post|_thread)?)&gt;((?:(?!&lt;\/topic_a(?:_post|_thread)?&gt;).)+)&lt;\/topic_a(?:_post|_thread)?&gt;', do_thread_a_change, data_end[0])
            data_end[0] = re.sub(r'&lt;topic_call&gt;@(?P<in>(?:(?!&lt;\/topic_call&gt;).)+)&lt;\/topic_call&gt;', '<a href="/w/user:\\g<in>">@\\g<in></a>', data_end[0])

        if data_type == 'backlink':
            mode = ''
            if re.search('^user:', doc_name):
                mode = 'user'
            elif re.search('^file:', doc_name):
                mode = 'file'
            elif re.search('^category:', doc_name):
                mode = 'category'

            backlink = data_end[2]['backlink'] if 'backlink' in data_end[2] else []
            backlinks.replace_for_document(doc_name, backlink)

            link_count = 0
            if 'link_count' in data_end[2]:
                link_count = data_end[2]['link_count']

            document_meta.upsert(doc_name, 'link_count', str(link_count))

            if mode != '':
                document_meta.upsert(doc_name, 'doc_type', mode)
            elif 'redirect' in data_end[2] and data_end[2]['redirect'] == 1:
                document_meta.upsert(doc_name, 'doc_type', 'redirect')
            else:
                document_meta.upsert(doc_name, 'doc_type', '')

        return [data_end[0], data_end[1], data_end[2]]
