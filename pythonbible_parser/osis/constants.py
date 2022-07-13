from __future__ import annotations

import pythonbible as bible

# noinspection SpellCheckingInspection
BOOK_IDS: dict[bible.Book, str] = {
    bible.Book.GENESIS: "Gen",
    bible.Book.EXODUS: "Exod",
    bible.Book.LEVITICUS: "Lev",
    bible.Book.NUMBERS: "Num",
    bible.Book.DEUTERONOMY: "Deut",
    bible.Book.JOSHUA: "Josh",
    bible.Book.JUDGES: "Judg",
    bible.Book.RUTH: "Ruth",
    bible.Book.SAMUEL_1: "1Sam",
    bible.Book.SAMUEL_2: "2Sam",
    bible.Book.KINGS_1: "1Kgs",
    bible.Book.KINGS_2: "2Kgs",
    bible.Book.CHRONICLES_1: "1Chr",
    bible.Book.CHRONICLES_2: "2Chr",
    bible.Book.EZRA: "Ezra",
    bible.Book.NEHEMIAH: "Neh",
    bible.Book.ESTHER: "Esth",
    bible.Book.JOB: "Job",
    bible.Book.PSALMS: "Ps",
    bible.Book.PROVERBS: "Prov",
    bible.Book.ECCLESIASTES: "Eccl",
    bible.Book.SONG_OF_SONGS: "Song",
    bible.Book.ISAIAH: "Isa",
    bible.Book.JEREMIAH: "Jer",
    bible.Book.LAMENTATIONS: "Lam",
    bible.Book.EZEKIEL: "Ezek",
    bible.Book.DANIEL: "Dan",
    bible.Book.HOSEA: "Hos",
    bible.Book.JOEL: "Joel",
    bible.Book.AMOS: "Amos",
    bible.Book.OBADIAH: "Obad",
    bible.Book.JONAH: "Jonah",
    bible.Book.MICAH: "Mic",
    bible.Book.NAHUM: "Nah",
    bible.Book.HABAKKUK: "Hab",
    bible.Book.ZEPHANIAH: "Zeph",
    bible.Book.HAGGAI: "Hag",
    bible.Book.ZECHARIAH: "Zech",
    bible.Book.MALACHI: "Mal",
    bible.Book.MATTHEW: "Matt",
    bible.Book.MARK: "Mark",
    bible.Book.LUKE: "Luke",
    bible.Book.JOHN: "John",
    bible.Book.ACTS: "Acts",
    bible.Book.ROMANS: "Rom",
    bible.Book.CORINTHIANS_1: "1Cor",
    bible.Book.CORINTHIANS_2: "2Cor",
    bible.Book.GALATIANS: "Gal",
    bible.Book.EPHESIANS: "Eph",
    bible.Book.PHILIPPIANS: "Phil",
    bible.Book.COLOSSIANS: "Col",
    bible.Book.THESSALONIANS_1: "1Thess",
    bible.Book.THESSALONIANS_2: "2Thess",
    bible.Book.TIMOTHY_1: "1Tim",
    bible.Book.TIMOTHY_2: "2Tim",
    bible.Book.TITUS: "Titus",
    bible.Book.PHILEMON: "Phlm",
    bible.Book.HEBREWS: "Heb",
    bible.Book.JAMES: "Jas",
    bible.Book.PETER_1: "1Pet",
    bible.Book.PETER_2: "2Pet",
    bible.Book.JOHN_1: "1John",
    bible.Book.JOHN_2: "2John",
    bible.Book.JOHN_3: "3John",
    bible.Book.JUDE: "Jude",
    bible.Book.REVELATION: "Rev",
    # bible.Book.BARUCH: "Bar",
    # bible.Book.ADDITIONS_TO_DANIEL: "AddDan",
    # bible.Book.PRAYER_OF_AZARIAH: "PrAzar",
    # bible.Book.BEL_AND_THE_DRAGON: "Bel",
    # bible.Book.SONG_OF_THE_THREE_YOUNG_MEN: "SgThree",
    # bible.Book.SUSANNA: "Sus",
    bible.Book.ESDRAS_1: "1Esd",
    # bible.Book.ESDRAS_2: "2Esd",
    # bible.Book.ADDITIONS_TO_ESTHER: "AddEsth",
    # bible.Book.EPISTLE_OF_JEREMIAH: "EpJer",
    # bible.Book.JUDITH: "Jdt",
    bible.Book.MACCABEES_1: "1Macc",
    bible.Book.MACCABEES_2: "2Macc",
    # bible.Book.MACCABEES_3: "3Macc",
    # bible.Book.MACCABEES_4: "4Macc",
    # bible.Book.PRAYER_OF_MANASSEH: "PrMan",
    bible.Book.ECCLESIASTICUS: "Sir",
    bible.Book.TOBIT: "Tobit",
    bible.Book.WISDOM_OF_SOLOMON: "Wis",
}


def get_book_by_id(book_id: str) -> bible.Book:
    for next_book, next_book_id in BOOK_IDS.items():
        if book_id == next_book_id:
            return next_book

    raise bible.InvalidBookError
