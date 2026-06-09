from __future__ import annotations

from dataclasses import dataclass

from opennamu_forge.presentation.shared.sql_dialect import re
from opennamu_forge.presentation.text_helpers import number_check


@dataclass(frozen=True)
class SectionEditData:
    content: str
    where: str
    apply: str


def resolve_section_edit_data(data: str, section: int | str, markup: str) -> SectionEditData:
    if section == "" or markup not in ("namumark", "namumark_beta"):
        return SectionEditData(data, "", "X")

    section_number = int(section)
    count = 1
    data_section = "\n" + data + "\n"
    data_match_re = r"\n((={1,6})(#?) ?([^\n]+)=)\n"

    while 1:
        data_match = re.search(data_match_re, data_section)
        if not data_match:
            return SectionEditData("", "", "X")

        if count > section_number:
            return SectionEditData("", "", "X")

        if section_number == count:
            data_section_sub = data_section
            data_section_sub = re.sub(
                data_match_re,
                ("." * (len(data_match.group(0)) - 1)) + "\n",
                data_section_sub,
                count=1,
            )
            data_match_plus = re.search(data_match_re, data_section_sub)
            if data_match_plus:
                return SectionEditData(
                    data[data_match.span()[0] : data_match_plus.span()[0] - 1],
                    str(data_match.span()[0]) + "," + str(data_match_plus.span()[0] - 1),
                    "O",
                )

            return SectionEditData(data[data_match.span()[0] :], str(data_match.span()[0]) + ",inf", "O")

        data_section = re.sub(
            data_match_re,
            ("." * (len(data_match.group(0)) - 1)) + "\n",
            data_section,
            count=1,
        )
        count += 1


def apply_section_edit_content(
    *,
    original_content: str,
    section_content: str,
    section_where: str,
    section_apply: str,
) -> str:
    if section_apply == "X" or section_where == "":
        return section_content

    data_match_where = section_where.split(",")
    if len(data_match_where) != 2:
        return section_content

    data_match_a = int(number_check(data_match_where[0]))
    data_match_b: int | str = data_match_where[1]
    if data_match_b != "inf":
        data_match_b = int(number_check(data_match_b))

    try:
        if data_match_b != "inf":
            return original_content[:data_match_a] + section_content + original_content[data_match_b:]

        return original_content[:data_match_a] + section_content
    except Exception:
        return section_content
