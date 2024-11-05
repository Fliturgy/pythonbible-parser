from __future__ import annotations

import re
from pathlib import Path

import pytest
import pythonbible as bible

from pythonbible_parser.osis.osis_parser import OSISParser

CURRENT_FOLDER: Path = Path(__file__).parent
DATA_FOLDER: Path = CURRENT_FOLDER / "data"
OUTPUT_FOLDER: Path = CURRENT_FOLDER / "output"


test_data = [
    (
        bible.Version.AMERICAN_KING_JAMES,
        "en",
        "akjv.xml",
        [
            (
                1001001,
                "1. In the beginning God created the heaven and the earth.",
            ),
            (
                66022021,
                "21. The grace of our Lord Jesus Christ be with you all. Amen.",
            ),
        ],
    ),
    (
        bible.Version.AMERICAN_STANDARD,
        "en",
        "asv.xml",
        [
            (
                1001001,
                "1. In the beginning God created the heavens and the earth.",
            ),
            (
                66022021,
                "21. The grace of the Lord Jesus be with the saints. Amen.",
            ),
        ],
    ),
    (
        bible.Version.BIBLE_IN_BASIC_ENGLISH,
        "en",
        "bbe.xml",
        [
            (
                1001001,
                "1. At the first God made the heaven and the earth.",
            ),
            (
                66022021,
                "21. The grace of the Lord Jesus be with the saints. So be it.",
            ),
        ],
    ),
    (
        bible.Version.WORLWIDE_ENGLISH,
        "en",
        "bwe.xml",
        [
            (
                40001001,
                "1. Here are the names of the people in the family line from which "
                "Jesus Christ came. He came from Davids family. He came from Abrahams "
                "family.",
            ),
            (
                66022021,
                "21. May the love and mercy of the Lord Jesus bless you all. Amen.",
            ),
        ],
    ),
    (
        bible.Version.DARBY,
        "en",
        "darby.xml",
        [
            (
                1001001,
                "1. In the beginning God created the heavens and the earth.",
            ),
            (
                66022021,
                "21. The grace of the Lord Jesus Christ [be] with all the saints.",
            ),
        ],
    ),
    (
        bible.Version.DIAGLOT_NT,
        "en",
        "diaglot.xml",
        [
            (
                40001001,
                "1. A record of descent of Jesus Anointed, son of David, son of "
                "Abraham.",
            ),
            (
                66022021,
                "21. The favor of the Lord Jesus Anointed, with all of the holy ones.",
            ),
        ],
    ),
    (
        bible.Version.DOUAY_RHEIMS,
        "en",
        "dour.xml",
        [
            (
                1001001,
                "1. In the beginning God created heaven, and earth.",
            ),
            (
                66022021,
                "21. The grace of our Lord Jesus Christ be with you all. Amen.",
            ),
        ],
    ),
    (
        bible.Version.ROTHERHAM,
        "en",
        "roth.xml",
        [
            (
                1001001,
                "1. In the beginning, God created the heavens and the earth.",
            ),
            (
                66022021,
                "21. The favour of the Lord Jesus  Christ  be with the saints.",
            ),
        ],
    ),
    (
        bible.Version.GENEVA,
        "en",
        "gb.xml",
        [
            (
                1001001,
                "1. In the beginning God created the heaven and the earth.",
            ),
            (
                66022021,
                "21. The grace of our Lord Jesus Christ [be] with you all. Amen.",
            ),
        ],
    ),
    (
        bible.Version.KING_JAMES,
        "en",
        "kjv.xml",
        [
            (
                1001001,
                "1. In the beginning God created the heaven and the earth.",
            ),
            (
                66022021,
                "21. The grace of our Lord Jesus Christ be with you all. Amen.",
            ),
        ],
    ),
    (
        bible.Version.LEESER,
        "en",
        "leeser.xml",
        [
            (
                1001001,
                "1. In the beginning God created the heaven and the earth.",
            ),
            (
                39004006,
                "6. And he shall turn back the heart of the fathers to the children, "
                "and the heart of the children to their fathers: lest I come and smite "
                "the earth with a curse.",
            ),
        ],
    ),
    (
        bible.Version.LIVING_ORACLES_NT,
        "en",
        "lont.xml",
        [
            (
                40001001,
                "1. The History of Jesus Christ, Son of David, Son of Abraham.",
            ),
            (
                66022021,
                "21. May the favor of the Lord Jesus Christ be with all the saints!",
            ),
        ],
    ),
    (
        bible.Version.KING_JAMES_MODERN_1963,
        "en",
        "mkjv1962.xml",
        [
            (
                1001001,
                "1. In the beginning God created the heavens and the earth.",
            ),
            (
                66022021,
                "21. The grace of our Lord Jesus Christ [be] with all of you. Amen.",
            ),
        ],
    ),
    (
        bible.Version.MONTGOMERY_NT,
        "en",
        "mont.xml",
        [
            (
                40001001,
                "1. The book of the generation of Jesus Christ, the son of David, the "
                "son of Abraham.",
            ),
            (
                66022021,
                "21. The grace of the Lord Jesus Christ be with the saints!",
            ),
        ],
    ),
    (
        bible.Version.NEW_HEART,
        "en",
        "nheb.xml",
        [
            (
                1001001,
                "1. In the beginning God created the heavens and the earth.",
            ),
            (
                66022021,
                "21. The grace of the Lord Jesus be with all.",
            ),
        ],
    ),
    (
        bible.Version.OPEN_ENGLISH,
        "en",
        "oeb.xml",
        [
            (
                40001001,
                "1. A genealogy of Jesus Christ, a descendant of David and Abraham.",
            ),
            (
                66022021,
                "21. May the blessing of the Lord Jesus Christ, be with his people.",
            ),
        ],
    ),
    (
        bible.Version.ETHERIDGE,
        "en",
        "etheridge.xml",
        [
            (
                40001001,
                "1. THE RECORD of the generation of Jeshu the Meshicha, the son of "
                "David, son of Abraham.",
            ),
            (
                66022021,
                "21. The grace of our Lord Jeshu Meshiha be with all the saints. Amen.",
            ),
        ],
    ),
    (
        bible.Version.REVISED_WEBSTER,
        "en",
        "rwebster.xml",
        [
            (
                1001001,
                "1. In the beginning God created the heaven and the earth.",
            ),
            (
                66022021,
                "21. The grace of our Lord Jesus Christ be with you all. Amen.",
            ),
        ],
    ),
    (
        bible.Version.REVISED_YOUNGS,
        "en",
        "rylt.xml",
        [
            (
                40001001,
                "1. A roll of the birth of Jesus Christ, son of David, son of Abraham.",
            ),
            (
                66022021,
                "21. The grace of our Lord Jesus Christ is with you all. Amen.",
            ),
        ],
    ),
    (
        bible.Version.KING_JAMES_UPDATED,
        "en",
        "ukjv.xml",
        [
            (
                1001001,
                "1. In the beginning God created the heaven and the earth.",
            ),
            (
                66022021,
                "21. The grace of our Lord Jesus Christ be with you all. Amen.",
            ),
        ],
    ),
    (
        bible.Version.WEBSTER,
        "en",
        "wbs.xml",
        [
            (
                1001001,
                "1. In the beginning God created the heaven and the earth.",
            ),
            (
                66022021,
                "21. The grace of our Lord Jesus Christ be with you all. Amen.",
            ),
        ],
    ),
    (
        bible.Version.WESLEY_NT,
        "en",
        "wesley.xml",
        [
            (
                40001001,
                "1. The book of the generation of Jesus Christ, the Son of David, the "
                "Son of Abraham.",
            ),
            (
                66022021,
                "21. The grace of the Lord Jesus be with you all.",
            ),
        ],
    ),
    (
        bible.Version.WEYMOUTH_NT,
        "en",
        "wmth.xml",
        [
            (
                40001001,
                "1. The Genealogy of Jesus Christ, the son of David, the son of "
                "Abraham.",
            ),
            (
                66022021,
                "21. The grace of the Lord Jesus be with God's people.",
            ),
        ],
    ),
    (
        bible.Version.TYNDALE,
        "en",
        "tyndale.xml",
        [
            (
                1001001,
                "1. In the begynnynge God created heaven and erth.",
            ),
            (
                66022021,
                "21. The grace of oure lorde Iesu Christ be with you all. Amen.",
            ),
        ],
    ),
    (
        bible.Version.WORLD_ENGLISH,
        "en",
        "web.xml",
        [
            (
                1001001,
                "1. In the beginning God created the heavens and the earth.",
            ),
            (
                66022021,
                "21. The grace of the Lord Jesus be with all the saints. Amen.",
            ),
        ],
    ),
    (
        bible.Version.WYCLIFFE,
        "en",
        "wycliffe.xml",
        [
            (
                1001001,
                "1. In the bigynnyng God made of nouyt heuene and erthe.",
            ),
            (
                66022021,
                "21. The grace of oure Lord Jhesu Crist be with you alle. Amen.",
            ),
        ],
    ),
    (
        bible.Version.YOUNGS,
        "en",
        "ylt.xml",
        [
            (
                1001001,
                "1. In the beginning of God`s preparing the heavens and the  earth --",
            ),
            (
                66022021,
                "21. The grace of our Lord Jesus Christ [is] with you all.  Amen.",
            ),
        ],
    ),
    # (
    #     bible.Version.REINA_VALERA_1989,
    #     "es",
    #     "rva.xml",
    #     [
    #         (
    #             1001001,
    #             "1. En el principio creó Dios los cielos y la tierra.",
    #         ),
    #         (
    #             66022021,
    #             "21. La gracia de nuestro Señor Jesús sea con todos.",
    #         ),
    #     ],
    # ),
]


@pytest.mark.parametrize(
    ("version", "language", "file_name", "verses"),
    test_data,
)
def test_alternate_osis_files(
    version: bible.Version,
    language: str,
    file_name: str,
    verses: list[tuple[int, str]],
) -> None:
    # Given an alternate ASV OSIS file
    osis_file = DATA_FOLDER / "public-domain-versions" / language / file_name

    # When parsing the OSIS file
    parser = OSISParser(version, osis_file=osis_file)
    parser.parse()

    # Then the parser has the correct version and the text is as expected
    assert parser.version == version

    parsed_bible = bible.Bible(
        parser.version,
        parser.plain_text,
        parser.plain_text_verse_start_indices,
        parser.plain_text_verse_end_indices,
        parser.max_verses,
    )

    for verse_id, expected_verse in verses:
        actual_verse = parsed_bible.get_scripture(verse_id)
        assert actual_verse == expected_verse

    # parser.write()


@pytest.mark.xfail(
    reason="KJV has minor differences, and ASV alternate has some errors.",
)
@pytest.mark.parametrize(
    ("version", "filename"),
    [
        (bible.Version.KING_JAMES, "kjv.xml"),
        (bible.Version.AMERICAN_STANDARD, "asv.xml"),
    ],
)
def test_kjv_bible_data(version: bible.Version, filename: str) -> None:
    original_parser = OSISParser(version)
    original_parser.parse()

    alternate_file = DATA_FOLDER / "public-domain-versions" / "en" / filename
    alternate_parser = OSISParser(version, osis_file=alternate_file)
    alternate_parser.parse()

    differences_actual = {}
    differences_expected = {}

    valid: bool = True

    original_start_indices = original_parser.plain_text_readers_verse_start_indices

    for verse_id, original_start in original_start_indices.items():
        original_end = original_parser.plain_text_readers_verse_end_indices[verse_id]
        original_verse = original_parser.plain_text_readers[original_start:original_end]
        clean_original_verse = clean_string(original_verse)

        alternate_start = alternate_parser.plain_text_readers_verse_start_indices[
            verse_id
        ]
        alternate_end = alternate_parser.plain_text_readers_verse_end_indices[verse_id]
        alternate_verse = alternate_parser.plain_text_readers[
            alternate_start:alternate_end
        ]
        clean_alternate_verse = clean_string(alternate_verse)

        if clean_original_verse != clean_alternate_verse:
            differences_actual[verse_id] = original_verse.strip()
            differences_expected[verse_id] = alternate_verse.strip()
            valid = False

    # if not valid:
    #     write_differences_output(version, differences_actual, differences_expected)

    assert valid


def clean_string(input_string: str) -> str:
    cleaned_string = re.sub(r"[^a-zA-Z0-9]", "", input_string)
    return cleaned_string.lower()


def write_differences_output(
    version: bible.Version,
    original_values: dict[int, str],
    alternate_values: dict[int, str],
) -> None:
    if not OUTPUT_FOLDER.exists():
        OUTPUT_FOLDER.mkdir()

    original_filename = OUTPUT_FOLDER / f"{version.value}-original.txt"

    with original_filename.open(mode="w", encoding="utf-8") as original_file:
        for verse_id, text in original_values.items():
            original_file.write(f"{verse_id}\t{text}\n\n")

    alternate_filename = Path(OUTPUT_FOLDER / f"{version.value}-alternate.txt")

    with alternate_filename.open(mode="w", encoding="utf-8") as alternate_file:
        for verse_id, text in alternate_values.items():
            alternate_file.write(f"{verse_id}\t{text}\n\n")
