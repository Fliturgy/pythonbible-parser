"""Contains the parser for OSIS format files."""

from __future__ import annotations

from datetime import datetime
from datetime import timezone
from pathlib import Path
from typing import Any

import pythonbible as bible
from defusedxml import ElementTree

from pythonbible_parser.osis.constants import BOOK_IDS
from pythonbible_parser.osis.osis_book_parser import OSISBookParser
from pythonbible_parser.osis.osis_utilities import get_namespace

CURRENT_FOLDER: Path = Path(__file__).parent
INPUT_FOLDER: Path = CURRENT_FOLDER / "versions"
OUTPUT_FOLDER: Path = CURRENT_FOLDER / "output"

XPATH_BOOK: str = ".//xmlns:div[@osisID='{}']"


class OSISParser:
    """Parse files containing scripture text in the OSIS format.

    OSISParser extends BibleParser and contains all the functionality necessary
    to parse XML files that are in the OSIS format.
    """

    version: bible.Version

    html: str
    html_readers: str
    html_notes: str
    plain_text: str
    plain_text_readers: str
    plain_text_notes: str

    html_verse_start_indices: dict[int, int]
    html_readers_verse_start_indices: dict[int, int]
    html_notes_verse_start_indices: dict[int, int]
    plain_text_verse_start_indices: dict[int, int]
    plain_text_readers_verse_start_indices: dict[int, int]
    plain_text_notes_verse_start_indices: dict[int, int]

    html_verse_end_indices: dict[int, int]
    html_readers_verse_end_indices: dict[int, int]
    html_notes_verse_end_indices: dict[int, int]
    plain_text_verse_end_indices: dict[int, int]
    plain_text_readers_verse_end_indices: dict[int, int]
    plain_text_notes_verse_end_indices: dict[int, int]

    short_titles: dict[bible.Book, str]
    long_titles: dict[bible.Book, str]

    max_verses: dict[bible.Book, dict[int, int]]

    def __init__(
        self: OSISParser,
        version: bible.Version,
        osis_file: Path | None = None,
    ) -> None:
        """Initialize the OSIS parser.

        Set the version, the element tree from the appropriate version XML file,
        and the namespaces.

        :param version:
        """
        self.version = version

        if not osis_file:
            osis_file = INPUT_FOLDER / f"{version.value.lower()}.xml"

        self.tree: ElementTree = ElementTree.parse(osis_file.resolve())
        self.namespaces: dict[str, str] = {
            "xmlns": get_namespace(self.tree.getroot().tag),
        }

        self.html = ""
        self.html_readers = ""
        self.html_notes = ""
        self.plain_text = ""
        self.plain_text_readers = ""
        self.plain_text_notes = ""

        self.html_verse_start_indices = {}
        self.html_readers_verse_start_indices = {}
        self.html_notes_verse_start_indices = {}
        self.plain_text_verse_start_indices = {}
        self.plain_text_readers_verse_start_indices = {}
        self.plain_text_notes_verse_start_indices = {}

        self.html_verse_end_indices = {}
        self.html_readers_verse_end_indices = {}
        self.html_notes_verse_end_indices = {}
        self.plain_text_verse_end_indices = {}
        self.plain_text_readers_verse_end_indices = {}
        self.plain_text_notes_verse_end_indices = {}

        self.short_titles = {}
        self.long_titles = {}

        self.max_verses = {}

    def parse(self: OSISParser) -> None:
        """Parse the XML input file."""
        html_offset: int = 0
        html_readers_offset: int = 0
        html_notes_offset: int = 0
        plain_text_offset: int = 0
        plain_text_readers_offset: int = 0
        plain_text_notes_offset: int = 0

        for book in bible.Book:
            book_element = self._get_book_element(book)

            if book_element is None:
                continue

            book_parser = OSISBookParser(
                book_element,
                html_offset,
                html_readers_offset,
                html_notes_offset,
                plain_text_offset,
                plain_text_readers_offset,
                plain_text_notes_offset,
            )
            book_parser.parse()

            self.html += book_parser.html
            self.html_readers += book_parser.html_readers
            self.html_notes += book_parser.html_notes
            self.plain_text += book_parser.plain_text
            self.plain_text_readers += book_parser.plain_text_readers
            self.plain_text_notes += book_parser.plain_text_notes

            html_offset = len(self.html)
            html_readers_offset = len(self.html_readers)
            html_notes_offset = len(self.html_notes)
            plain_text_offset = len(self.plain_text)
            plain_text_readers_offset = len(self.plain_text_readers)
            plain_text_notes_offset = len(self.plain_text_notes)

            self.html_verse_start_indices.update(book_parser.html_verse_start_indices)
            self.html_readers_verse_start_indices.update(
                book_parser.html_readers_verse_start_indices,
            )
            self.html_notes_verse_start_indices.update(
                book_parser.html_notes_verse_start_indices,
            )
            self.plain_text_verse_start_indices.update(
                book_parser.plain_text_verse_start_indices,
            )
            self.plain_text_readers_verse_start_indices.update(
                book_parser.plain_text_readers_verse_start_indices,
            )
            self.plain_text_notes_verse_start_indices.update(
                book_parser.plain_text_notes_verse_start_indices,
            )

            self.html_verse_end_indices.update(book_parser.html_verse_end_indices)
            self.html_readers_verse_end_indices.update(
                book_parser.html_readers_verse_end_indices,
            )
            self.html_notes_verse_end_indices.update(
                book_parser.html_notes_verse_end_indices,
            )
            self.plain_text_verse_end_indices.update(
                book_parser.plain_text_verse_end_indices,
            )
            self.plain_text_readers_verse_end_indices.update(
                book_parser.plain_text_readers_verse_end_indices,
            )
            self.plain_text_notes_verse_end_indices.update(
                book_parser.plain_text_notes_verse_end_indices,
            )

            self.short_titles[book] = book_parser.short_title or book.title
            self.long_titles[book] = book_parser.title.strip() or book.title

            self.max_verses[book] = book_parser.max_verses

    def write(self: OSISParser, output_folder: Path = OUTPUT_FOLDER) -> None:
        """Write the content out to file(s)."""
        version_str: str = self.version.value.lower()
        version_folder: Path = output_folder / version_str

        for folder in (output_folder, version_folder):
            folder_path = Path(folder)

            if not folder_path.exists():
                folder_path.mkdir()

        _write_bible_file(
            version_folder,
            "html_bible.py",
            self.version,
            self.html,
            self.html_verse_start_indices,
            self.html_verse_end_indices,
            self.max_verses,
            True,
        )
        _write_bible_file(
            version_folder,
            "html_readers_bible.py",
            self.version,
            self.html_readers,
            self.html_readers_verse_start_indices,
            self.html_readers_verse_end_indices,
            self.max_verses,
            True,
        )
        _write_bible_file(
            version_folder,
            "html_notes_bible.py",
            self.version,
            self.html_notes,
            self.html_notes_verse_start_indices,
            self.html_notes_verse_end_indices,
            self.max_verses,
            True,
        )
        _write_bible_file(
            version_folder,
            "plain_text_bible.py",
            self.version,
            self.plain_text,
            self.plain_text_verse_start_indices,
            self.plain_text_verse_end_indices,
            self.max_verses,
        )
        _write_bible_file(
            version_folder,
            "plain_text_readers_bible.py",
            self.version,
            self.plain_text_readers,
            self.plain_text_readers_verse_start_indices,
            self.plain_text_readers_verse_end_indices,
            self.max_verses,
        )
        _write_bible_file(
            version_folder,
            "plain_text_notes_bible.py",
            self.version,
            self.plain_text_notes,
            self.plain_text_notes_verse_start_indices,
            self.plain_text_notes_verse_end_indices,
            self.max_verses,
        )

        _write_init_file(version_folder, self.short_titles, self.long_titles)

    def _get_book_element(self: OSISParser, book: bible.Book) -> Any:
        xpath: str = XPATH_BOOK.format(BOOK_IDS.get(book))
        return self.tree.find(xpath, namespaces=self.namespaces)


def _file_header() -> str:
    return (
        f"# This file was automatically generated by the pythonbible-parser package on "
        f"{datetime.now(timezone.utc)}.\n\n"
    )


def _get_max_verses_string(max_verses: dict[bible.Book, dict[int, int]]) -> str:
    max_verses_string = ",".join(
        [f"Book.{book.name}: {chapters}" for book, chapters in max_verses.items()],
    )
    return f"{{{max_verses_string}}}"


def _write_bible_file(
    folder: Path,
    filename: str,
    version: bible.Version,
    bible_text: str,
    verse_start_indices: dict[int, int],
    verse_end_indices: dict[int, int],
    max_verses: dict[bible.Book, dict[int, int]],
    is_html: bool = False,
) -> None:
    file_path = folder / filename

    with file_path.open(mode="w", encoding="utf-8") as writer:
        writer.write(_file_header())
        writer.write("from pythonbible.bible.bible import Bible\n")
        writer.write("from pythonbible.books import Book\n")
        writer.write("from pythonbible.versions import Version\n\n\n")
        writer.write("bible = Bible(\n")
        writer.write(f"    Version.{version.name},\n")
        writer.write(f'    """{bible_text}""",\n')
        writer.write(f"    {verse_start_indices},\n")
        writer.write(f"    {verse_end_indices},\n")
        writer.write(f"    {_get_max_verses_string(max_verses)},\n")
        writer.write(f"    {is_html},\n")
        writer.write(")\n")


BIBLES_CONTENT: str = """from pythonbible.versions import Version

from . import html_bible
from . import html_notes_bible
from . import html_readers_bible
from . import plain_text_bible
from . import plain_text_notes_bible
from . import plain_text_readers_bible


BIBLES = {{
    Version.{}: {{
         \"html\": html_bible.bible,
         \"html_notes\": html_notes_bible.bible,
         \"html_readers\": html_readers_bible.bible,
         \"plain_text\": plain_text_bible.bible,
         \"plain_text_notes\": plain_text_notes_bible.bible,
         \"plain_text_readers\": plain_text_readers_bible.bible,
    }}
}}
"""


def _titles_dict_to_string(titles: dict[bible.Book, str]) -> str:
    return (
        "{\n"
        + ",\n".join(
            [f'    Book.{book.name}: "{title}"' for book, title in titles.items()],
        )
        + ",\n}"
    )


def _write_init_file(
    folder: Path,
    short_titles: dict[bible.Book, str],
    long_titles: dict[bible.Book, str],
) -> None:
    file_path = folder / "__init__.py"

    with file_path.open(mode="w", encoding="utf-8") as writer:
        writer.write(_file_header())
        writer.write("from pythonbible.books import Book\n\n\n")
        writer.write(f"SHORT_TITLES = {_titles_dict_to_string(short_titles)}\n\n")
        writer.write(f"LONG_TITLES = {_titles_dict_to_string(long_titles)}\n")
