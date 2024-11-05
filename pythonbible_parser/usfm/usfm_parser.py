from pyparsing import Group
from pyparsing import OneOrMore
from pyparsing import Optional
from pyparsing import Suppress
from pyparsing import Word
from pyparsing import alphanums
from pyparsing import restOfLine


# Define data structures for USFM elements
class UsfmElement:
    def __init__(self, marker, content=None) -> None:
        self.marker = marker
        self.content = content

    def __repr__(self) -> str:
        return f"UsfmElement(marker={self.marker}, content={self.content})"


# Define parsers for USFM elements
marker = Suppress("\\") + Word(f"{alphanums}-")("marker")
text_content = restOfLine("content")
element = Group(marker + Optional(text_content))("element")

# Define parser for a USFM document
usfm_parser = OneOrMore(element)


# Example usage
def parse_usfm(input_text) -> list[UsfmElement]:
    parsed_elements = usfm_parser.parseString(input_text, parseAll=True)
    return [
        UsfmElement(parsed_element.marker, parsed_element.content)
        for parsed_element in parsed_elements
    ]


# Example USFM input
usfm_input = """
\\c 1
\\v 1 In the beginning...
\\v 2 And God said...
\\c 2
\\v 1 And on the seventh day...
"""


if __name__ == "__main__":
    # Parse the USFM document
    parsed_document = parse_usfm(usfm_input)

    for element in parsed_document:
        print(element)
