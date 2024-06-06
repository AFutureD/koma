from __future__ import annotations

from enum import IntEnum
from typing import Sequence

from pydantic import BaseModel

from .attachment import NoteAttachment
from ...core import RenderAble, TextRenderer, Model


class ParagraphStyleType(IntEnum):
    Title = 0
    Heading = 1
    Subheading = 2
    CodeBlock = 4

    DotList = 100
    DashList = 101
    NumberList = 102
    TodoList = 103

    def group_identifier(self):
        return self.value if not self.should_newline else 100

    @property
    def should_newline(self):
        return self.value >= 100


class FontStyle(IntEnum):
    Normal = 0
    Bold = 1
    Italic = 2
    Bold_Italic = 3


class CheckInfo(Model):
    done: bool
    uuid: str

    def __hash__(self):
        return hash((self.done.__hash__(), self.uuid.__hash__()))

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "CheckInfo(done: {}, uuid: {})".format(self.done, self.uuid)


class ParagraphStyle(Model):
    style_type: None | ParagraphStyleType = None
    indent_level: int = 0
    check_info: None | CheckInfo = None
    quote: bool = False

    def is_same_block(self, previous: ParagraphStyle):

        # two lines are to-do list
        if self.check_info is not None and previous.check_info is not None:
            return True

        # two lines are quote
        if self.quote or previous.quote:
            return self.quote and previous.quote

        if self.style_type is None or previous.style_type is None:
            return True
        # elif self.style_type is not None and previous.style_type is None:
        #     return True
        # elif self.style_type is None and previous.style_type is not None:
        #     return True
        elif self.style_type is not None and previous.style_type is not None:
            return self.style_type.group_identifier() >= previous.style_type.group_identifier()
        else:
            return False

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"DocParagraphStyle(style_type: {self.style_type}, indent_level: {self.indent_level}, check_info: {self.check_info}, quote: {self.quote})"


class TextAttribute(Model):
    paragraph_style: None | ParagraphStyle = None

    font_style: None | FontStyle = None
    font_name: None | str = None  # useless for now
    underlined: None | bool = None
    strike_through: None | bool = None
    link: None | str = None
    attachment_identifier: None | str = None
    attachment: None | NoteAttachment = None

    def __hash__(self):
        return hash(
            (
                self.font_style, self.font_name,
                self.underlined, self.strike_through, self.link,
                self.attachment
            )
        )

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"NoteAttribute({self.model_dump(exclude_none=True)})"

    def inline_identifier(self):
        return self.__hash__()

    def __eq__(self, other):
        if not isinstance(other, TextAttribute):
            return False

        return (
            self.paragraph_style == other.paragraph_style
            and self.font_style == other.font_style
            and self.font_name == other.font_name
            and self.underlined == other.underlined
            and self.strike_through == other.strike_through
            and self.link == other.link
            and self.attachment == other.attachment
        )


class AttributeText(RenderAble, Model):
    start_index: int
    length: int
    text: str

    attribute: TextAttribute

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "DocAttributeText(text: {}, from: {}, len: {}, attr: {})".format(
            self.text.__repr__(), self.start_index, self.length, self.attribute
        )

    def render(self, renderer: TextRenderer):
        if self.attribute and self.attribute.attachment:
            self.attribute.attachment.render(renderer)

        super().render(renderer)

    def splitlines(self, keepends: bool = True) -> Sequence[AttributeText]:
        """
        Split the text into lines and return a list of DocAttributeText.

        Example:
        ```
        "foo" -> ["foo"]
        "foo\n" -> ["foo"]
        "foo\n\n" -> ["foo", ""]
        "\n\n" -> ["", ""]
        "foo\nbar\nbaz" -> [foo, bar, baz]
        "foo\nbar\nbaz\n" -> [foo, bar, baz]
        ```
        """

        snippets = self.text.splitlines(keepends)

        split_snippets = []
        for snip in snippets:
            idx = self.text.index(snip)

            snip_attr = AttributeText(start_index = idx, length = len(snip), text = snip, attribute = self.attribute)

            split_snippets.append(snip_attr)

        return split_snippets
