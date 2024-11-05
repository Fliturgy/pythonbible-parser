from __future__ import annotations

import json
from pathlib import Path

import pytest
import pythonbible as pb

from pythonbible_parser.osis.osis_parser import OSISParser

CURRENT_FOLDER: Path = Path(__file__).parent
DATA_FOLDER: Path = CURRENT_FOLDER / "data"
OUTPUT_FOLDER: Path = CURRENT_FOLDER / "output"


def _import_bible_data(file_name: str) -> dict[int, str]:
    bible_data = {}

    with (DATA_FOLDER / file_name).open() as json_file:
        json_data = json.load(json_file)
        result_set = json_data["resultset"]
        row = result_set["row"]

        for element in row:
            verse_id, _, _, _, text = element["field"]
            bible_data[verse_id] = text

    return bible_data


@pytest.mark.xfail(
    reason="The KJV test data seems to be from a slightly different version.",
)
@pytest.mark.parametrize(
    ("version", "baseline"),
    [
        (pb.Version.KING_JAMES, _import_bible_data("t_kjv.json")),
        (pb.Version.AMERICAN_STANDARD, _import_bible_data("t_asv.json")),
    ],
)
def test_bible_data(version: pb.Version, baseline: dict[int, str]) -> None:
    parser = OSISParser(version)
    parser.parse()

    differences_actual = {}
    differences_expected = {}

    valid: bool = True

    for verse_id, start in parser.plain_text_readers_verse_start_indices.items():
        expected = baseline.get(verse_id, "").strip()
        end = parser.plain_text_readers_verse_end_indices[verse_id]
        actual = parser.plain_text_readers[start:end].replace("`", "'").strip()

        if actual != expected:
            differences_actual[verse_id] = actual
            differences_expected[verse_id] = expected

            valid = False

    # if not valid:
    #     write_differences_output(version, differences_actual, differences_expected)

    assert valid


def write_differences_output(
    version: pb.Version,
    differences_actual: dict[int, str],
    differences_expected: dict[int, str],
) -> None:
    if not OUTPUT_FOLDER.exists():
        OUTPUT_FOLDER.mkdir()

    actual_file_path = OUTPUT_FOLDER / f"{version.value}-actual.txt"

    with actual_file_path.open(mode="w", encoding="utf-8") as actual_file:
        for verse_id, text in differences_actual.items():
            actual_file.write(f"{verse_id}\t{text}\n\n")

    expected_file_path = OUTPUT_FOLDER / f"{version.value}-expected.txt"

    with expected_file_path.open(mode="w", encoding="utf-8") as expected_file:
        for verse_id, text in differences_expected.items():
            expected_file.write(f"{verse_id}\t{text}\n\n")
