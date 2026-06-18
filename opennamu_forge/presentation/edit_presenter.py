from __future__ import annotations

import asyncio
import html

import flask

from opennamu_forge.application.dto.settings import SettingKey
from opennamu_forge.presentation.captcha_helpers import captcha_get
from opennamu_forge.presentation.dependencies import (
    get_document_meta_repository,
    get_wiki_settings_service,
)
from opennamu_forge.presentation.edit_toolbar_helpers import edit_button, ip_warning
from opennamu_forge.presentation.rendering.render_helpers import render_set
from opennamu_forge.presentation.response_helpers import get_lang
from opennamu_forge.presentation.shared.sql_dialect import get_main_skin_set


async def edit_timeout(name, content, timeout=3):
    try:
        await asyncio.wait_for(
            render_set(
                doc_name=name,
                doc_data=content,
            ),
            timeout=timeout,
        )

        return 0
    except asyncio.TimeoutError:
        return 1


async def edit_editor(ip, data_main="", do_type="edit", addon="", name="", markup_selector_html=""):
    document_meta = get_document_meta_repository()
    wiki_settings = get_wiki_settings_service()

    monaco_editor_top = ""
    div = ""

    if do_type == "edit":
        help_text = wiki_settings.get(SettingKey.EDIT_HELP)
        div = document_meta.get(name, "document_top")
    elif do_type == "bbs":
        help_text = wiki_settings.get(SettingKey.BBS_HELP)
    elif do_type == "bbs_comment":
        help_text = wiki_settings.get(SettingKey.BBS_COMMENT_HELP)
    else:
        help_text = wiki_settings.get(SettingKey.TOPIC_TEXT)

    if do_type == "bbs_comment":
        do_type = "thread"
    elif do_type == "bbs":
        do_type = "edit"

    p_text = html.escape(help_text) if help_text != "" else await get_lang("default_edit_help")

    monaco_editor_top += (
        '<div class="opennamu_forge_edit_actionbar opennamu_forge_edit_actionbar_temp">'
        '<a class="opennamu_forge_edit_action" href="javascript:opennamu_forge_do_editor_temp_save();">'
        + await get_lang("load_temp_save")
        + '</a>'
        '<a class="opennamu_forge_edit_action" href="javascript:opennamu_forge_do_editor_temp_save_load();">'
        + await get_lang("load_temp_save_load")
        + '</a>'
        '</div>'
    )
    monaco_editor_top += '<hr class="main_hr">'

    darkmode = flask.request.cookies.get("main_css_darkmode", "0")
    monaco_thema = "vs-dark" if darkmode == "1" else ""

    monaco_on = get_main_skin_set(flask.session, "main_css_monaco", ip)
    editor_display = ['style="display: none;"' for _ in range(3)]
    if monaco_on == "use":
        editor_display[1] = ""
    else:
        editor_display[0] = ""

    monaco_editor_top += '<span class="__ON_SELECT_DIV__"><select class="__ON_SELECT__" onclick="do_sync_monaco_and_textarea();" id="opennamu_forge_select_editor" onchange="opennamu_forge_edit_turn_off_monaco();">'
    monaco_editor_top += '<option value="default" ' + ("selected" if editor_display[0] == "" else "") + ">" + await get_lang("default") + "</option>"
    monaco_editor_top += '<option value="monaco" ' + ("selected" if editor_display[1] == "" else "") + ">" + await get_lang("monaco_editor") + "</option>"
    monaco_editor_top += "</select></span> "
    monaco_editor_top += markup_selector_html

    textarea_size = "opennamu_forge_textarea_500" if do_type == "edit" else "opennamu_forge_textarea_100"

    out_field = await captcha_get() + await ip_warning() + addon
    if out_field != "":
        out_field += '<hr class="main_hr">'

    return '''
        <textarea class="__ON_TEXTAREA__" style="display: none;" id="opennamu_forge_edit_origin" name="doc_data_org">''' + html.escape(data_main) + '''</textarea>
        <div>
            ''' + monaco_editor_top + '''
            <hr class="main_hr">
            ''' + await edit_button() + '''
            <div id="opennamu_forge_editor_user_button"></div>
        </div>
        
        ''' + div + '''

        <div id="opennamu_forge_monaco_editor" class="''' + textarea_size + '''" ''' + editor_display[1] + '''></div>
        <textarea id="opennamu_forge_edit_textarea" class="''' + textarea_size + ''' __ON_TEXTAREA__" ''' + editor_display[0] + ''' name="content" placeholder="''' + p_text + '''">''' + html.escape(data_main) + '''</textarea>
        <hr class="main_hr">
        ''' + out_field + '''
        
        <script>
            window.addEventListener('DOMContentLoaded', function() {
                do_stop_exit();
                do_paste_image();
                do_monaco_init("''' + monaco_thema + '''");
                opennnamu_do_user_editor();
            });
        </script>
                        
        <button class="__ON_BUTTON__" id="opennamu_forge_save_button" type="submit" onclick="do_stop_exit_release();">''' + await get_lang("send") + '''</button>
        <button class="__ON_BUTTON__" id="opennamu_forge_preview_button" type="button" onclick="opennamu_forge_do_editor_preview();">''' + await get_lang("preview") + '''</button>
        <hr class="main_hr">

        <div id="opennamu_forge_preview_area"></div>
    '''
