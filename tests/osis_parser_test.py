from __future__ import annotations

from functools import lru_cache

import pythonbible as bible

from pythonbible_parser.osis.osis_parser import OSISParser


@lru_cache()
def get_parser(version: bible.Version) -> OSISParser:
    parser = OSISParser(version)
    parser.parse()
    return parser


@lru_cache()
def get_plain_text_bible(version: bible.Version) -> bible.Bible:
    parser = get_parser(version)
    return bible.Bible(
        parser.version,
        parser.plain_text,
        parser.plain_text_verse_start_indices,
        parser.plain_text_verse_end_indices,
        parser.max_verses,
    )


@lru_cache()
def get_plain_text_readers_bible(version: bible.Version) -> bible.Bible:
    parser = get_parser(version)
    return bible.Bible(
        parser.version,
        parser.plain_text_readers,
        parser.plain_text_readers_verse_start_indices,
        parser.plain_text_readers_verse_end_indices,
        parser.max_verses,
    )


@lru_cache()
def get_plain_text_notes_bible(version: bible.Version) -> bible.Bible:
    parser = get_parser(version)
    return bible.Bible(
        parser.version,
        parser.plain_text_notes,
        parser.plain_text_notes_verse_start_indices,
        parser.plain_text_notes_verse_end_indices,
        parser.max_verses,
    )


@lru_cache()
def get_html_bible(version: bible.Version) -> bible.Bible:
    parser = get_parser(version)
    return bible.Bible(
        parser.version,
        parser.html,
        parser.html_verse_start_indices,
        parser.html_verse_end_indices,
        parser.max_verses,
        is_html=True,
    )


@lru_cache()
def get_html_readers_bible(version: bible.Version) -> bible.Bible:
    parser = get_parser(version)
    return bible.Bible(
        parser.version,
        parser.html_readers,
        parser.html_readers_verse_start_indices,
        parser.html_readers_verse_end_indices,
        parser.max_verses,
        is_html=True,
    )


@lru_cache()
def get_html_notes_bible(version: bible.Version) -> bible.Bible:
    parser = get_parser(version)
    return bible.Bible(
        parser.version,
        parser.html_notes,
        parser.html_notes_verse_start_indices,
        parser.html_notes_verse_end_indices,
        parser.max_verses,
        is_html=True,
    )


def test_exodus_20_3_asv() -> None:
    """Test for https://github.com/avendesora/pythonbible/issues/9."""
    # Given the verse id for Exodus 20:3
    verse_id: int = 2020003

    # When we get the verse text using the ASV parser
    version: bible.Version = bible.Version.AMERICAN_STANDARD
    plain_bible: bible.Bible = get_plain_text_bible(version)
    plain_readers_bible: bible.Bible = get_plain_text_readers_bible(version)
    plain_notes_bible: bible.Bible = get_plain_text_notes_bible(version)
    html_bible: bible.Bible = get_html_bible(version)
    html_readers_bible: bible.Bible = get_html_readers_bible(version)
    html_notes_bible: bible.Bible = get_html_notes_bible(version)
    verse_text: str = plain_bible.get_scripture(verse_id)
    verse_text_readers: str = plain_readers_bible.get_scripture(verse_id)
    verse_text_notes: str = plain_notes_bible.get_scripture(verse_id)
    verse_text_html: str = html_bible.get_scripture(verse_id)
    verse_text_html_readers: str = html_readers_bible.get_scripture(verse_id)
    verse_text_html_notes: str = html_notes_bible.get_scripture(verse_id)

    # Then the verse text is not missing any words.
    assert verse_text == "3. Thou shalt have no other gods before me."
    assert verse_text_readers == "Thou shalt have no other gods before me."
    assert verse_text_notes == verse_text
    assert (
        verse_text_html == "<p><sup>3</sup> Thou shalt have no other gods before me."
        "</p>"
    )
    assert verse_text_html_readers == "<p>Thou shalt have no other gods before me.</p>"
    assert verse_text_html_notes == verse_text_html


def test_mark_9_38_kjv() -> None:
    """Test for https://github.com/avendesora/pythonbible/issues/12."""
    # Given the verse id for Mark 9:38
    verse_id: int = 41009038

    # When we get the verse text using the KJV parser
    version: bible.Version = bible.Version.KING_JAMES
    plain_bible: bible.Bible = get_plain_text_bible(version)
    plain_readers_bible: bible.Bible = get_plain_text_readers_bible(version)
    plain_notes_bible: bible.Bible = get_plain_text_notes_bible(version)
    html_bible: bible.Bible = get_html_bible(version)
    html_readers_bible: bible.Bible = get_html_readers_bible(version)
    html_notes_bible: bible.Bible = get_html_notes_bible(version)
    verse_text: str = plain_bible.get_scripture(verse_id)
    verse_text_readers: str = plain_readers_bible.get_scripture(verse_id)
    verse_text_notes: str = plain_notes_bible.get_scripture(verse_id)
    verse_text_html: str = html_bible.get_scripture(verse_id)
    verse_text_html_readers: str = html_readers_bible.get_scripture(verse_id)
    verse_text_html_notes: str = html_notes_bible.get_scripture(verse_id)

    # Then there are no errors and the verse text is as expected
    assert (
        verse_text == "38. And John answered him, saying, Master, we saw one casting "
        "out devils in thy name, and he followeth not us: and we forbad him, because "
        "he followeth not us."
    )
    assert (
        verse_text_readers == "And John answered him, saying, Master, we saw one "
        "casting out devils in thy name, and he followeth not us: and we forbad him, "
        "because he followeth not us."
    )
    assert verse_text_notes == verse_text
    assert (
        verse_text_html == "<p><sup>38</sup> And John answered him, saying, Master, we "
        "saw one casting out devils in thy name, and he followeth not us: and we "
        "forbad him, because he followeth not us.</p>"
    )
    assert (
        verse_text_html_readers == "<p>And John answered him, saying, Master, we saw "
        "one casting out devils in thy name, and he followeth not us: and we forbad "
        "him, because he followeth not us.</p>"
    )
    assert verse_text_html_notes == verse_text_html


def test_mark_9_43_kjv() -> None:
    """Test for https://github.com/avendesora/pythonbible/issues/16."""
    # Given the verse id for Mark 9:43
    verse_id: int = 41009043

    # When we get the verse text using the KJV parser
    version: bible.Version = bible.Version.KING_JAMES
    plain_bible: bible.Bible = get_plain_text_bible(version)
    plain_readers_bible: bible.Bible = get_plain_text_readers_bible(version)
    plain_notes_bible: bible.Bible = get_plain_text_notes_bible(version)
    html_bible: bible.Bible = get_html_bible(version)
    html_readers_bible: bible.Bible = get_html_readers_bible(version)
    html_notes_bible: bible.Bible = get_html_notes_bible(version)
    verse_text: str = plain_bible.get_scripture(verse_id)
    verse_text_readers: str = plain_readers_bible.get_scripture(verse_id)
    verse_text_notes: str = plain_notes_bible.get_scripture(verse_id)
    verse_text_html: str = html_bible.get_scripture(verse_id)
    verse_text_html_readers: str = html_readers_bible.get_scripture(verse_id)
    verse_text_html_notes: str = html_notes_bible.get_scripture(verse_id)

    # Then there are no errors and the verse text is as expected
    assert (
        verse_text == "43. And if thy hand offend thee, cut it off: it is better for "
        "thee to enter into life maimed, than having two hands to go into hell, into "
        "the fire that never shall be quenched:"
    )
    assert (
        verse_text_readers == "And if thy hand offend thee, cut it off: it is better "
        "for thee to enter into life maimed, than having two hands to go into hell, "
        "into the fire that never shall be quenched:"
    )
    assert verse_text_notes == verse_text
    assert (
        verse_text_html == "<p><sup>43</sup> And if thy hand offend thee, cut it off: "
        "it is better for thee to enter into life maimed, than having two hands to go "
        "into hell, into the fire that never shall be quenched:</p>"
    )
    assert (
        verse_text_html_readers == "<p>And if thy hand offend thee, cut it off: it is "
        "better for thee to enter into life maimed, than having two hands to go into "
        "hell, into the fire that never shall be quenched:</p>"
    )
    assert verse_text_html_notes == verse_text_html


def test_matthew_17_21_asv() -> None:
    """Test for https://github.com/avendesora/pythonbible/issues/19."""
    # Given the verse id for Matthew 17:21
    verse_id: int = 40017021

    # When we get the verse text using the ASV parser
    version: bible.Version = bible.Version.AMERICAN_STANDARD
    plain_bible: bible.Bible = get_plain_text_bible(version)
    plain_readers_bible: bible.Bible = get_plain_text_readers_bible(version)
    plain_notes_bible: bible.Bible = get_plain_text_notes_bible(version)
    html_bible: bible.Bible = get_html_bible(version)
    html_readers_bible: bible.Bible = get_html_readers_bible(version)
    html_notes_bible: bible.Bible = get_html_notes_bible(version)
    verse_text: str = plain_bible.get_scripture(verse_id)
    verse_text_readers: str = plain_readers_bible.get_scripture(verse_id)
    verse_text_notes: str = plain_notes_bible.get_scripture(verse_id)
    verse_text_html: str = html_bible.get_scripture(verse_id)
    verse_text_html_readers: str = html_readers_bible.get_scripture(verse_id)
    verse_text_html_notes: str = html_notes_bible.get_scripture(verse_id)

    # Then there are no errors and the verse text is as expected
    assert verse_text == "21."
    assert not verse_text_readers
    assert (
        verse_text_notes == "21. But this kind goeth not out save by prayer and "
        "fasting."
    )
    assert verse_text_html == "<p><sup>21</sup></p>"
    assert not verse_text_html_readers
    assert (
        verse_text_html_notes == "<p><sup>21</sup> But this kind goeth not out save by "
        "prayer and fasting.</p>"
    )


def test_1_chronicles_16_8_kjv() -> None:
    """Test for https://github.com/avendesora/pythonbible/issues/50."""
    # Given the verse id for 1 Chronicles 16:8
    verse_id: int = 13016008

    # When we get the verse text using the KJV parser
    version: bible.Version = bible.Version.KING_JAMES
    plain_bible: bible.Bible = get_plain_text_bible(version)
    plain_readers_bible: bible.Bible = get_plain_text_readers_bible(version)
    plain_notes_bible: bible.Bible = get_plain_text_notes_bible(version)
    html_bible: bible.Bible = get_html_bible(version)
    html_readers_bible: bible.Bible = get_html_readers_bible(version)
    html_notes_bible: bible.Bible = get_html_notes_bible(version)
    verse_text: str = plain_bible.get_scripture(verse_id)
    verse_text_readers: str = plain_readers_bible.get_scripture(verse_id)
    verse_text_notes: str = plain_notes_bible.get_scripture(verse_id)
    verse_text_html: str = html_bible.get_scripture(verse_id)
    verse_text_html_readers: str = html_readers_bible.get_scripture(verse_id)
    verse_text_html_notes: str = html_notes_bible.get_scripture(verse_id)

    # Then there are no errors and the verse text is as expected
    assert (
        verse_text == "8. Give thanks unto the LORD, call upon his name, make known "
        "his deeds among the people."
    )
    assert (
        verse_text_readers == "Give thanks unto the LORD, call upon his name, make "
        "known his deeds among the people."
    )
    assert verse_text_notes == verse_text
    assert (
        verse_text_html == "<p><sup>8</sup> Give thanks unto the LORD, call upon his "
        "name, make known his deeds among the people.</p>"
    )
    assert (
        verse_text_html_readers == "<p>Give thanks unto the LORD, call upon his name, "
        "make known his deeds among the people.</p>"
    )
    assert verse_text_html_notes == verse_text_html


def test_write() -> None:
    # actually test this once the functionality is more complete
    get_parser(bible.Version.KING_JAMES).write()
    get_parser(bible.Version.AMERICAN_STANDARD).write()
