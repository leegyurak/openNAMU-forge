import pytest

from opennamu_forge.presentation.edit_section_helpers import (
    apply_section_edit_content,
    resolve_section_edit_data,
)


@pytest.mark.parametrize(
    ("section", "expected_content", "expected_where", "expected_apply"),
    [
        (1, "= First =\nAlpha", "0,15", "O"),
        (2, "= Second =\nBeta", "16,inf", "O"),
        (3, "", "", "X"),
    ],
)
def test_resolve_section_edit_data는_namumark_section_범위를_계산한다(
    section,
    expected_content,
    expected_where,
    expected_apply,
):
    data = "= First =\nAlpha\n= Second =\nBeta"

    result = resolve_section_edit_data(data, section, "namumark")

    assert result.content == expected_content
    assert result.where == expected_where
    assert result.apply == expected_apply


def test_resolve_section_edit_data는_지원하지_않는_markup이면_전체_본문을_반환한다():
    result = resolve_section_edit_data("content", 1, "markdown")

    assert result.content == "content"
    assert result.where == ""
    assert result.apply == "X"


@pytest.mark.parametrize(
    ("section_where", "section_apply", "expected"),
    [
        ("0,15", "O", "replacement\n= Second =\nBeta"),
        ("16,inf", "O", "= First =\nAlpha\nreplacement"),
        ("16,inf", "X", "replacement"),
        ("", "O", "replacement"),
    ],
)
def test_apply_section_edit_content는_숨은_section_범위로_본문을_교체한다(
    section_where,
    section_apply,
    expected,
):
    original_content = "= First =\nAlpha\n= Second =\nBeta"

    result = apply_section_edit_content(
        original_content=original_content,
        section_content="replacement",
        section_where=section_where,
        section_apply=section_apply,
    )

    assert result == expected
