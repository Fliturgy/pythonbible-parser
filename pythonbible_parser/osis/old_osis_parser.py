"""Contains the parser for OSIS format files."""

from __future__ import annotations

import ast
from functools import lru_cache
from pathlib import Path
from typing import Any

from defusedxml import ElementTree
from pythonbible import Book
from pythonbible import InvalidVerseError
from pythonbible import Version
from pythonbible import get_book_chapter_verse
from pythonbible import get_verse_id

from pythonbible_parser.bible_parser import BibleParser
from pythonbible_parser.bible_parser import sort_paragraphs
from pythonbible_parser.osis.constants import BOOK_IDS
from pythonbible_parser.osis.osis_utilities import OSISID
from pythonbible_parser.osis.osis_utilities import get_element_tail
from pythonbible_parser.osis.osis_utilities import get_element_text
from pythonbible_parser.osis.osis_utilities import get_element_text_and_tail
from pythonbible_parser.osis.osis_utilities import get_namespace
from pythonbible_parser.osis.osis_utilities import parse_osis_id
from pythonbible_parser.osis.osis_utilities import strip_namespace_from_tag

XML_FOLDER: Path = Path(__file__).parent / "versions"

XPATH_BOOK: str = ".//xmlns:div[@osisID='{}']"
XPATH_BOOK_TITLE: str = f"{XPATH_BOOK}/xmlns:title"
XPATH_VERSE: str = ".//xmlns:verse[@osisID='{}.{}.{}']"
XPATH_VERSE_PARENT: str = f"{XPATH_VERSE}/.."


class OldOSISParser(BibleParser):
    """Parse files containing scripture text in the OSIS format.

    OSISParser extends BibleParser and contains all the functionality necessary
    to parse XML files that are in the OSIS format.
    """

    def __init__(self: OldOSISParser, version: Version) -> None:
        """Initialize the OSIS parser.

        Set the version, the element tree from the appropriate version XML file,
        and the namespaces.

        :param version:
        """
        super().__init__(version)

        self.tree: ElementTree = ElementTree.parse(
            XML_FOLDER / f"{self.version.value.lower()}.xml",
        )
        self.namespaces: dict[str, str] = {
            "xmlns": get_namespace(self.tree.getroot().tag),
        }

    @lru_cache()
    def get_book_title(self: OldOSISParser, book: Book) -> str:
        """Given a book, return the full title for that book from the XML file.

        :param book:
        :return: the full title string
        """
        book_title_element = self._get_book_title_element(book)
        return book_title_element.text or ""

    @lru_cache()
    def get_short_book_title(self: OldOSISParser, book: Book) -> str:
        """Given a book, return the short title for that book from the XML file.

        :param book:
        :return: the short title string
        """
        book_title_element = self._get_book_title_element(book)
        return book_title_element.get("short") or ""

    def get_scripture_passage_text(
        self: OldOSISParser,
        verse_ids: list[int],
        **kwargs: Any | None,
    ) -> dict[Book, dict[int, list[str]]]:
        """Get the scripture passage for the given verse ids.

        Given a list of verse ids, return the structured scripture text passage
        organized by book, chapter, and paragraph.

        If the include_verse_number keyword argument is True, include the verse
        numbers in the scripture passage; otherwise, do not include them.

        :param verse_ids:
        :param kwargs
        :return: the scripture passage text in a dictionary of books to
        dictionary of chapter numbers to lists of paragraph strings
        """
        if verse_ids is None or not verse_ids:
            return {}

        # Sort the verse ids and the convert it into a tuple so it's hashable
        verse_ids.sort()
        verse_ids_tuple: tuple[int, ...] = tuple(verse_ids)

        # keyword arguments
        include_verse_number: bool = ast.literal_eval(
            str(kwargs.get("include_verse_number", True))
        )

        return self._get_scripture_passage_text_memoized(
            verse_ids_tuple,
            include_verse_number,
        )

    def verse_text(
        self: OldOSISParser,
        verse_id: int,
        **kwargs: Any | None,
    ) -> str:
        """Get the scripture text for the given verse id.

        Given a verse id, return the string scripture text passage for that verse.

        If the include_verse_number keyword argument is True, include the verse
        numbers in the scripture passage; otherwise, do not include them.

        :param verse_id:
        :param kwargs:
        :return:
        """
        if verse_id is None:
            msg = "Verse id cannot be None."
            raise InvalidVerseError(msg)

        # keyword arguments
        include_verse_number: bool = ast.literal_eval(
            str(kwargs.get("include_verse_number", True))
        )

        return self._get_verse_text_memoized(verse_id, include_verse_number)

    @lru_cache()
    def _get_book_title_element(self: OldOSISParser, book: Book) -> Any:
        xpath: str = XPATH_BOOK_TITLE.format(BOOK_IDS.get(book))
        return self.tree.find(xpath, namespaces=self.namespaces)

    @lru_cache()
    def _get_scripture_passage_text_memoized(
        self: OldOSISParser,
        verse_ids: tuple[int],
        include_verse_number: bool,
    ) -> dict[Book, dict[int, list[str]]]:
        paragraphs: dict[Book, dict[int, list[str]]] = _get_paragraphs(
            self.tree,
            self.namespaces,
            verse_ids,
            include_verse_number,
        )

        return sort_paragraphs(paragraphs)

    @lru_cache()
    def _get_verse_text_memoized(
        self: OldOSISParser,
        verse_id: int,
        include_verse_number: bool,
    ) -> str:
        verse_ids = (verse_id,)
        paragraphs: dict[Book, dict[int, list[str]]] = _get_paragraphs(
            self.tree,
            self.namespaces,
            verse_ids,
            include_verse_number,
        )

        verse_text: str = ""

        for chapters in paragraphs.values():
            for chapter_paragraphs in chapters.values():
                verse_text = chapter_paragraphs[0]
                break

        return verse_text


def _get_paragraphs(
    tree: ElementTree,
    namespaces: dict[str, str],
    verse_ids: tuple[int, ...],
    include_verse_number: bool,
) -> dict[Book, dict[int, list[str]]]:
    current_verse_id: int = verse_ids[0]
    book: Book
    chapter: int
    verse: int
    book, chapter, verse = get_book_chapter_verse(current_verse_id)
    paragraph_element = tree.find(
        XPATH_VERSE_PARENT.format(BOOK_IDS.get(book), chapter, verse),
        namespaces,
    )
    paragraph: str
    paragraph, current_verse_id = _get_paragraph_from_element(
        paragraph_element,
        verse_ids,
        current_verse_id,
        include_verse_number,
    )
    current_verse_index: int = verse_ids.index(current_verse_id) + 1
    paragraph_dictionary: dict[Book, dict[int, list[str]]] = {}

    if current_verse_index < len(verse_ids):
        paragraph_dictionary = _get_paragraphs(
            tree,
            namespaces,
            verse_ids[current_verse_index:],
            include_verse_number,
        )

    book_dictionary: dict[int, list[str]] = paragraph_dictionary.get(book, {})
    chapter_list: list[str] = book_dictionary.get(int(chapter), [])
    chapter_list.insert(0, paragraph)
    book_dictionary[int(chapter)] = chapter_list
    paragraph_dictionary[book] = book_dictionary

    return paragraph_dictionary


@lru_cache()
def _get_paragraph_from_element(
    paragraph_element: Any,
    verse_ids: tuple[int, ...],
    current_verse_id: int,
    include_verse_number: bool,
) -> tuple[str, int]:
    new_current_verse_id: int = current_verse_id
    paragraph: str = ""
    skip_till_next_verse: bool = False
    child_paragraph: str

    for child_element in list(paragraph_element):
        (
            child_paragraph,
            skip_till_next_verse,
            new_current_verse_id,
        ) = _handle_child_element(
            child_element,
            verse_ids,
            skip_till_next_verse,
            new_current_verse_id,
            include_verse_number,
        )

        if not child_paragraph:
            continue

        if paragraph and not paragraph.endswith(" "):
            paragraph += " "

        paragraph += child_paragraph

    return clean_paragraph(paragraph), new_current_verse_id


@lru_cache()
def _handle_child_element(
    child_element: Any,
    verse_ids: tuple[int, ...],
    skip_till_next_verse: bool,
    current_verse_id: int,
    include_verse_number: bool,
    inside_note: bool = False,
) -> tuple[str, bool, int]:
    tag: str = strip_namespace_from_tag(child_element.tag)

    if tag == "verse":
        return _handle_verse_tag(
            child_element,
            verse_ids,
            skip_till_next_verse,
            current_verse_id,
            include_verse_number,
        )

    if skip_till_next_verse:
        return "", skip_till_next_verse, current_verse_id

    if tag == "rdg":
        return (
            get_element_text(child_element),
            skip_till_next_verse,
            current_verse_id,
        )

    # If we are inside a note tag, only allow the "rdg" text to be included
    if inside_note:
        return "", skip_till_next_verse, current_verse_id

    if tag in {"w", "transChange"}:
        return (
            get_element_text_and_tail(child_element),
            skip_till_next_verse,
            current_verse_id,
        )

    paragraph: str = ""

    if tag == "q":
        paragraph += get_element_text_and_tail(child_element)

    new_current_verse_id: int = current_verse_id

    for grandchild_element in list(child_element):
        (
            grandchild_paragraph,
            skip_till_next_verse,
            new_current_verse_id,
        ) = _handle_child_element(
            grandchild_element,
            verse_ids,
            skip_till_next_verse,
            current_verse_id,
            include_verse_number,
            tag == "note",
        )

        paragraph += grandchild_paragraph

    if tag == "seg":
        paragraph += get_element_tail(child_element)

    return clean_paragraph(paragraph), skip_till_next_verse, new_current_verse_id


@lru_cache()
def _handle_verse_tag(
    child_element: Any,
    verse_ids: tuple[int, ...],
    skip_till_next_verse: bool,
    current_verse_id: int,
    include_verse_number: bool,
) -> tuple[str, bool, int]:
    paragraph: str = ""
    osis_id_str: str = child_element.get("osisID") or ".."

    if osis_id_str == "..":
        return paragraph, skip_till_next_verse, current_verse_id

    osis_id: OSISID = parse_osis_id(osis_id_str)
    verse_id: int = get_verse_id(
        Book(osis_id.book.value),
        int(osis_id.chapter),
        int(osis_id.verse),
    )

    if verse_id in verse_ids:
        if skip_till_next_verse:
            skip_till_next_verse = False

            if current_verse_id is not None and verse_id > current_verse_id + 1:
                paragraph += "... "

        if include_verse_number:
            paragraph += f"{osis_id.verse}. "

        paragraph += get_element_text_and_tail(child_element)

        return paragraph, skip_till_next_verse, verse_id

    skip_till_next_verse = True
    return paragraph, skip_till_next_verse, current_verse_id


@lru_cache()
def clean_paragraph(paragraph: str) -> str:
    cleaned_paragraph: str = paragraph.replace("¶", "").replace("  ", " ")
    return cleaned_paragraph.strip()
