from __future__ import annotations

import itertools
from datetime import datetime
from typing import Sequence, Annotated

from pydantic import BaseModel, SkipValidation, ConfigDict

from .text import ParagraphStyle, AttributeText
from ...core import RenderAble


class NoteContentLine(RenderAble, BaseModel):
    idx: int
    elements: Sequence[AttributeText]

    plain_text: str
    attribute: None | ParagraphStyle

    # def __init__(self, idx: int, elements: Sequence[AttributeText]):
    #     rebuilt_elements = self._rebuild_elements(elements)
    #     plain_text = "".join([element.text for element in rebuilt_elements])
    #     attribute = self._build_attribute(rebuilt_elements)
    #
    #     super().__init__(idx = idx, elements = elements, plain_text = plain_text, attribute = attribute)
    #
    #     self.idx = idx
    #     self.elements = rebuilt_elements
    #     self.plain_text = plain_text
    #     self.attribute = attribute

    @classmethod
    def of(cls, idx: int, elements: Sequence[AttributeText]) -> NoteContentLine:
        rebuilt_elements = cls._rebuild_elements(elements)
        plain_text = "".join([element.text for element in rebuilt_elements])
        attribute = cls._build_attribute(rebuilt_elements)

        return NoteContentLine(idx = idx, elements = rebuilt_elements, plain_text = plain_text, attribute = attribute)

    @staticmethod
    def _rebuild_elements(elements: Sequence[AttributeText]) -> Sequence[AttributeText]:
        """
        rebuild attribute's column index
        """

        grouped_element = itertools.groupby(elements, key = lambda x: x.attribute.inline_identifier())

        compressed_elements = []

        cur_column_idx = 0
        for _, group in grouped_element:
            group_list = list(group)
            length = sum([ele.length for ele in group_list])
            text = "".join([ele.text for ele in group_list])
            attribute = group_list[0].attribute

            attribute_text = AttributeText(start_index = cur_column_idx, length = length, text = text, attribute = attribute)
            compressed_elements.append(attribute_text)

            cur_column_idx += length

        return compressed_elements

    @staticmethod
    def _build_attribute(elements: Sequence[AttributeText]) -> ParagraphStyle | None:
        attribute = elements[0].attribute

        return attribute.paragraph_style if attribute is not None else None

    def __str__(self):
        return self.plain_text.__repr__()

    def is_same_paragraph(self, other: NoteContentLine | None):
        if other is None:
            return False

        if self.attribute is None and other.attribute is None:
            return True
        elif self.attribute is not None and other.attribute is None:
            return False
        elif self.attribute is None and other.attribute is not None:
            return False
        else:
            assert other.attribute is not None
            assert self.attribute is not None
            return self.attribute.is_same_paragraph(other.attribute)

    def is_paragraph_breaker(self):
        return self.plain_text == "\n"


class NoteContentParagraph(RenderAble, BaseModel):
    lines: Sequence[NoteContentLine]

    attribute: None | ParagraphStyle


class NoteContent(RenderAble, BaseModel):
    plan_text: str
    attributed_text: Sequence[AttributeText]
    paragraph_list: Sequence[NoteContentParagraph]


class Note(RenderAble, BaseModel):
    z_pk: int
    uuid: str
    navigation_link: str
    title: str
    folder_name: str
    modified_at: datetime
    preview: None | str
    account_pk: int
    locked: bool
    pinned: bool
    content: NoteContent

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return (f"Memory(z_pk: {self.z_pk}, uuid: {self.uuid}, modified_at: {self.modified_at}, "
                f"locked: {self.locked}, pinned: {self.pinned}, title: {self.title}, "
                f"folder_name: {self.folder_name}, account_name: {self.account_pk}, "
                f"url_scheme: `{self.navigation_link}`")

