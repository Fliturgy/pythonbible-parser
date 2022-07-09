"""Contains the parser for OSIS format files."""

import os
from functools import lru_cache
from typing import Dict, List, Tuple
from xml.etree.ElementTree import Element

from defusedxml import ElementTree
from pythonbible import (
    Book,
    InvalidVerseError,
    Version,
    get_book_chapter_verse,
    get_verse_id,
)

from ..bible_parser import BibleParser, sort_paragraphs
from .constants import BOOK_IDS, get_book_by_id

XML_FOLDER: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), "versions")

XPATH_BOOK: str = ".//xmlns:div[@osisID='{}']"
XPATH_BOOK_TITLE: str = f"{XPATH_BOOK}/xmlns:title"
XPATH_VERSE: str = ".//xmlns:verse[@osisID='{}.{}.{}']"
XPATH_VERSE_PARENT: str = f"{XPATH_VERSE}/.."


class OSISParser(BibleParser):
    """
    Parse files containing scripture text in the OSIS format.

    OSISParser extends BibleParser and contains all the functionality necessary
    to parse XML files that are in the OSIS format.
    """

    def __init__(self, version: Version) -> None:
        """
        Initialize the OSIS parser.

        Set the version, the element tree from the appropriate version XML file,
        and the namespaces.

        :param version:
        """
        super().__init__(version)

        self.tree: ElementTree = ElementTree.parse(
            os.path.join(XML_FOLDER, f"{self.version.value.lower()}.xml")
        )
        self.namespaces: Dict[str, str] = {
            "xmlns": _get_namespace(self.tree.getroot().tag)
        }

    @lru_cache()
    def get_book_title(self, book: Book) -> str:
        """
        Given a book, return the full title for that book from the XML file.

        :param book:
        :return: the full title string
        """
        book_title_element: Element = self._get_book_title_element(book)
        return book_title_element.text or ""

    @lru_cache()
    def get_short_book_title(self, book: Book) -> str:
        """
        Given a book, return the short title for that book from the XML file.

        :param book:
        :return: the short title string
        """
        book_title_element: Element = self._get_book_title_element(book)
        return book_title_element.get("short", "")

    @lru_cache()
    def _get_book_title_element(self, book: Book) -> Element:
        xpath: str = XPATH_BOOK_TITLE.format(BOOK_IDS.get(book))
        return self.tree.find(xpath, namespaces=self.namespaces)

    def get_scripture_passage_text(
        self, verse_ids: List[int], **kwargs
    ) -> Dict[Book, Dict[int, List[str]]]:
        """
        Get the scripture passage for the given verse ids.

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
        verse_ids_tuple: Tuple = tuple(verse_ids)

        # keyword arguments
        include_verse_number: bool = kwargs.get("include_verse_number", True)

        return self._get_scripture_passage_text_memoized(
            verse_ids_tuple, include_verse_number
        )

    @lru_cache()
    def _get_scripture_passage_text_memoized(
        self, verse_ids, include_verse_number
    ) -> Dict[Book, Dict[int, List[str]]]:
        paragraphs: Dict[Book, Dict[int, List[str]]] = _get_paragraphs(
            self.tree,
            self.namespaces,
            verse_ids,
            include_verse_number,
        )

        return sort_paragraphs(paragraphs)

    def get_verse_text(self, verse_id: int, **kwargs) -> str:
        """
        Get the scripture text for the given verse id.

        Given a verse id, return the string scripture text passage for that verse.

        If the include_verse_number keyword argument is True, include the verse
        numbers in the scripture passage; otherwise, do not include them.

        :param verse_id:
        :param kwargs:
        :return:
        """
        if verse_id is None:
            raise InvalidVerseError("Verse id cannot be None.")

        # keyword arguments
        include_verse_number: bool = kwargs.get("include_verse_number", True)

        return self._get_verse_text_memoized(verse_id, include_verse_number)

    @lru_cache()
    def _get_verse_text_memoized(
        self, verse_id: int, include_verse_number: bool
    ) -> str:
        paragraphs: Dict[Book, Dict[int, List[str]]] = _get_paragraphs(
            self.tree, self.namespaces, (verse_id,), include_verse_number
        )

        verse_text: str = ""

        for chapters in paragraphs.values():
            for chapter_paragraphs in chapters.values():
                verse_text = chapter_paragraphs[0]
                break

        return verse_text


@lru_cache()
def _get_namespace(tag: str) -> str:
    return tag[tag.index("{") + 1 : tag.index("}")]


@lru_cache()
def _strip_namespace_from_tag(tag: str) -> str:
    return tag.replace(_get_namespace(tag), "").replace("{", "").replace("}", "")


def _get_paragraphs(
    tree: ElementTree,
    namespaces: Dict[str, str],
    verse_ids: Tuple[int, ...],
    include_verse_number: bool,
) -> Dict[Book, Dict[int, List[str]]]:
    current_verse_id: int = verse_ids[0]
    book: Book
    chapter: int
    verse: int
    book, chapter, verse = get_book_chapter_verse(current_verse_id)
    paragraph_element: Element = tree.find(
        XPATH_VERSE_PARENT.format(BOOK_IDS.get(book), chapter, verse), namespaces
    )
    paragraphs: List[str]
    paragraphs, current_verse_id = _get_paragraph_from_element(
        paragraph_element,
        verse_ids,
        current_verse_id,
        include_verse_number,
    )
    current_verse_index: int = verse_ids.index(current_verse_id) + 1
    paragraph_dictionary: Dict[Book, Dict[int, List[str]]] = {}

    if current_verse_index < len(verse_ids):
        paragraph_dictionary = _get_paragraphs(
            tree,
            namespaces,
            verse_ids[current_verse_index:],
            include_verse_number,
        )

    book_dictionary: Dict[int, List[str]] = paragraph_dictionary.get(book, {})
    chapter_list: List[str] = book_dictionary.get(int(chapter), [])
    paragraphs.extend(chapter_list)
    book_dictionary[int(chapter)] = paragraphs
    paragraph_dictionary[book] = book_dictionary

    return paragraph_dictionary


@lru_cache()
def _get_paragraph_from_element(
    paragraph_element: Element,
    verse_ids: Tuple[int, ...],
    current_verse_id: int,
    include_verse_number: bool,
) -> Tuple[List[str], int]:
    new_current_verse_id: int = current_verse_id
    paragraphs: List[str] = []
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

        if len(child_paragraph) == 0:
            continue

        if len(paragraph) > 0 and not paragraph.endswith(" "):
            paragraph += " "

        paragraph += child_paragraph

    paragraphs.append(clean_paragraph(paragraph))
    return paragraphs, new_current_verse_id


@lru_cache()
def _handle_child_element(
    child_element: Element,
    verse_ids: Tuple[int, ...],
    skip_till_next_verse: bool,
    current_verse_id: int,
    include_verse_number: bool,
    inside_note: bool = False,
) -> Tuple[str, bool, int]:
    tag: str = _strip_namespace_from_tag(child_element.tag)

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
            _get_element_text(child_element),
            skip_till_next_verse,
            current_verse_id,
        )

    # If we are inside a note tag, only allow the "rdg" text to be included
    if inside_note:
        return "", skip_till_next_verse, current_verse_id

    if tag in {"w", "transChange"}:
        return (
            _get_element_text_and_tail(child_element),
            skip_till_next_verse,
            current_verse_id,
        )

    paragraph: str = ""

    if tag == "q":
        paragraph += _get_element_text_and_tail(child_element)

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
        paragraph += _get_element_tail(child_element)

    return clean_paragraph(paragraph), skip_till_next_verse, new_current_verse_id


@lru_cache()
def _handle_verse_tag(
    child_element: Element,
    verse_ids: Tuple[int, ...],
    skip_till_next_verse: bool,
    current_verse_id: int,
    include_verse_number: bool,
) -> Tuple[str, bool, int]:
    paragraph: str = ""
    osis_id: str = child_element.get("osisID", "..")

    if osis_id == "..":
        return paragraph, skip_till_next_verse, current_verse_id

    book_id: str
    chapter: str
    verse: str
    book_id, chapter, verse = osis_id.split(".")
    book: Book = get_book_by_id(book_id)
    verse_id: int = get_verse_id(book, int(chapter), int(verse))

    if verse_id in verse_ids:
        if skip_till_next_verse:
            skip_till_next_verse = False

            if current_verse_id is not None and verse_id > current_verse_id + 1:
                paragraph += "... "

        if include_verse_number:
            paragraph += f"{verse}. "

        paragraph += _get_element_text_and_tail(child_element)

        return paragraph, skip_till_next_verse, verse_id

    skip_till_next_verse = True
    return paragraph, skip_till_next_verse, current_verse_id


@lru_cache()
def _get_element_text_and_tail(element: Element) -> str:
    return _get_element_text(element) + _get_element_tail(element)


@lru_cache()
def _get_element_text(element: Element) -> str:
    return element.text.replace("\n", " ") if element.text else ""


@lru_cache()
def _get_element_tail(element: Element) -> str:
    return element.tail.replace("\n", " ") if element.tail else ""


@lru_cache()
def clean_paragraph(paragraph: str) -> str:
    cleaned_paragraph: str = paragraph.replace("¶", "").replace("  ", " ")
    return cleaned_paragraph.strip()
