from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

TitleCriteriaBuilder = Callable[[Any], tuple[Any, ...]]
TitleSpecKey = tuple[bool, bool, bool]


def _all_titles(title_column: Any) -> tuple[Any, ...]:
    return ()


def _without_user_pages(title_column: Any) -> tuple[Any, ...]:
    return (title_column.not_like("user:%"),)


def _without_file_pages(title_column: Any) -> tuple[Any, ...]:
    return (title_column.not_like("file:%"),)


def _without_category_pages(title_column: Any) -> tuple[Any, ...]:
    return (title_column.not_like("category:%"),)


def _without_user_and_file_pages(title_column: Any) -> tuple[Any, ...]:
    return (title_column.not_like("user:%"), title_column.not_like("file:%"))


def _without_user_and_category_pages(title_column: Any) -> tuple[Any, ...]:
    return (title_column.not_like("user:%"), title_column.not_like("category:%"))


def _without_file_and_category_pages(title_column: Any) -> tuple[Any, ...]:
    return (title_column.not_like("file:%"), title_column.not_like("category:%"))


def _without_user_file_and_category_pages(title_column: Any) -> tuple[Any, ...]:
    return (
        title_column.not_like("user:%"),
        title_column.not_like("file:%"),
        title_column.not_like("category:%"),
    )


@dataclass(frozen=True)
class WikiTitleSpec:
    key: TitleSpecKey = (False, False, False)

    @classmethod
    def all(cls) -> WikiTitleSpec:
        return _WIKI_TITLE_SPECS[(False, False, False)]

    @classmethod
    def exclude_user_pages(cls) -> WikiTitleSpec:
        return _WIKI_TITLE_SPECS[(True, False, False)]

    @classmethod
    def exclude_file_pages(cls) -> WikiTitleSpec:
        return _WIKI_TITLE_SPECS[(False, True, False)]

    @classmethod
    def exclude_category_pages(cls) -> WikiTitleSpec:
        return _WIKI_TITLE_SPECS[(False, False, True)]

    @classmethod
    def from_exclusions(
        cls,
        *,
        exclude_user_pages: bool = False,
        exclude_file_pages: bool = False,
        exclude_category_pages: bool = False,
    ) -> WikiTitleSpec:
        return _WIKI_TITLE_SPECS[(exclude_user_pages, exclude_file_pages, exclude_category_pages)]

    def criteria(self, title_column: Any) -> tuple[Any, ...]:
        return _WIKI_TITLE_CRITERIA[self.key](title_column)


_WIKI_TITLE_CRITERIA: dict[TitleSpecKey, TitleCriteriaBuilder] = {
    (False, False, False): _all_titles,
    (True, False, False): _without_user_pages,
    (False, True, False): _without_file_pages,
    (False, False, True): _without_category_pages,
    (True, True, False): _without_user_and_file_pages,
    (True, False, True): _without_user_and_category_pages,
    (False, True, True): _without_file_and_category_pages,
    (True, True, True): _without_user_file_and_category_pages,
}

_WIKI_TITLE_SPECS: dict[TitleSpecKey, WikiTitleSpec] = {
    (False, False, False): WikiTitleSpec((False, False, False)),
    (True, False, False): WikiTitleSpec((True, False, False)),
    (False, True, False): WikiTitleSpec((False, True, False)),
    (False, False, True): WikiTitleSpec((False, False, True)),
    (True, True, False): WikiTitleSpec((True, True, False)),
    (True, False, True): WikiTitleSpec((True, False, True)),
    (False, True, True): WikiTitleSpec((False, True, True)),
    (True, True, True): WikiTitleSpec((True, True, True)),
}
