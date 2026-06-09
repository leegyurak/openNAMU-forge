from __future__ import annotations

import html
from dataclasses import dataclass
from typing import Protocol


class ChallengeStatusReader(Protocol):
    def exists(self, user_id: str, name: str) -> bool: ...


class LanguageProvider(Protocol):
    async def __call__(self, data: str, safe: int = 0) -> str: ...


@dataclass(frozen=True)
class ChallengeCardSpec:
    setting_key: str
    icon: str
    title_key: str
    info_key: str


CHALLENGE_CARD_SPECS = (
    ChallengeCardSpec("challenge_first_contribute", "🔰", "challenge_title_first_contribute", "challenge_info_first_contribute"),
    ChallengeCardSpec("challenge_tenth_contribute", "📝", "challenge_title_tenth_contribute", "challenge_info_tenth_contribute"),
    ChallengeCardSpec("challenge_hundredth_contribute", "🖊️", "challenge_title_hundredth_contribute", "challenge_info_hundredth_contribute"),
    ChallengeCardSpec("challenge_thousandth_contribute", "🏅", "challenge_title_thousandth_contribute", "challenge_info_thousandth_contribute"),
    ChallengeCardSpec("challenge_first_discussion", "💬", "challenge_title_first_discussion", "challenge_info_first_discussion"),
    ChallengeCardSpec("challenge_tenth_discussion", "💡", "challenge_title_tenth_discussion", "challenge_info_tenth_discussion"),
    ChallengeCardSpec("challenge_hundredth_discussion", "📢", "challenge_title_hundredth_discussion", "challenge_info_hundredth_discussion"),
    ChallengeCardSpec("challenge_thousandth_discussion", "📜", "challenge_title_thousandth_discussion", "challenge_info_thousandth_discussion"),
    ChallengeCardSpec("challenge_admin", "☑️", "challenge_title_admin", "challenge_info_admin"),
)


def make_challenge_design(icon: str, title: str, info: str, disable: int = 0) -> str:
    if disable == 1:
        table_style = 'style="border: 2px solid green"'
    else:
        table_style = 'style="border: 2px solid red"'

    return '''
        <table id="main_table_set" ''' + table_style + '''>
            <tr>
                <td id="main_table_width_quarter" rowspan="2">
                    <span style="font-size: 64px;">''' + icon + '''</span>
                </td>
                <td>
                    <span style="font-size: 32px;">''' + title + '''</span>
                </td>
            </tr>
            <tr>
                <td>''' + info + '''</td>
        </table>
        <hr class="main_hr">
    '''


async def render_challenge_cards(user_id: str, status_reader: ChallengeStatusReader, get_lang: LanguageProvider) -> str:
    data_html_green = make_challenge_design(
        "🌳",
        await get_lang("challenge_title_register"),
        await get_lang("challenge_info_register", 1),
        1,
    )
    data_html_red = ""

    for spec in CHALLENGE_CARD_SPECS:
        disable = 1 if status_reader.exists(user_id, spec.setting_key) else 0
        data_html = make_challenge_design(
            spec.icon,
            await get_lang(spec.title_key),
            await get_lang(spec.info_key, 1),
            disable,
        )

        if disable == 1:
            data_html_green += data_html
        else:
            data_html_red += data_html

    return data_html_green + data_html_red


async def render_challenge_body(user_id: str, status_reader: ChallengeStatusReader, get_lang: LanguageProvider) -> str:
    return await render_challenge_cards(user_id, status_reader, get_lang) + '''
                <form method="post">
                    <div id="opennamu_forge_get_user_info">''' + html.escape(user_id) + '''</div>
                    <hr class="main_hr">
                    <button class="__ON_BUTTON__" id="opennamu_forge_save_button" type="submit">''' + await get_lang("reload") + '''</button>
                </form>
            '''
