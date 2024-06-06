from typing import List, Sequence
from koma.domain.models.note import NoteContentLine
from koma.domain.models.style import AttributeText, TextAttribute, ParagraphStyle
import pytest
import unittest

from koma.infra.helper.apple import build_content_lines, build_paragraph_list


class AppleFetcherTests(unittest.TestCase):
    
    def test_build_lines(self):
        nodes: Sequence[AttributeText] = [
            AttributeText(start_index=0, length=5, text="Hello ", attribute=TextAttribute()),
            AttributeText(start_index=5, length=5, text="World", attribute=TextAttribute()),
            AttributeText(start_index=10, length=2, text="!\n", attribute=TextAttribute()),
            AttributeText(start_index=12, length=1, text="\n", attribute=TextAttribute()),
            AttributeText(start_index=13, length=7, text="xixixi\n", attribute=TextAttribute()),
            AttributeText(start_index=20, length=2, text="ha", attribute=TextAttribute()),
            AttributeText(start_index=22, length=3, text="hx", attribute=TextAttribute()),
        ]

        lines: List[NoteContentLine] = build_content_lines(nodes)
        assert lines[0].plain_text == "Hello World!\n"
        assert lines[1].plain_text == "\n"
        assert lines[2].plain_text == "xixixi\n"
        assert lines[3].plain_text == "hahx"
    
    def test_build_paragraph(self):
        # build_paragraph_list
        lines: List[NoteContentLine] = [
            NoteContentLine(idx=1, plain_text="Hello World!\n", elements=[], attribute=ParagraphStyle())
        ]
        build_paragraph_list(lines)



        