from opennamu_forge.presentation.recent_change_presenter import recent_change_send_render


def test_recent_change_send_render는_empty_text를_br로_바꾼다():
    assert recent_change_send_render("") == "<br>"


def test_recent_change_send_render는_javascript_scheme을_제거한다():
    rendered = recent_change_send_render("javascript: https://example.test")

    assert "javascript:" not in rendered
    assert '<a href="https://example.test">' in rendered
