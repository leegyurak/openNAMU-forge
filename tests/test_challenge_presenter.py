import asyncio

from opennamu_forge.presentation.challenge_presenter import render_challenge_body


class FakeChallengeStatus:
    def exists(self, user_id, name):
        return name == "challenge_admin"


async def fake_get_lang(data, safe=0):
    return data if safe == 0 else data + ":" + str(safe)


def test_challenge_presenter는_카드와_reload_form을_렌더링한다():
    body = asyncio.run(render_challenge_body("alice<admin>", FakeChallengeStatus(), fake_get_lang))

    assert "challenge_title_register" in body
    assert "challenge_title_admin" in body
    assert 'style="border: 2px solid green"' in body
    assert 'style="border: 2px solid red"' in body
    assert "alice&lt;admin&gt;" in body
    assert "challenge_info_register:1" in body
