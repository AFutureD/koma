import unittest
import pytest

from koma.domain import ParagraphStyleType, ParagraphStyle, CheckInfo


class StyleTests(unittest.TestCase):
    def test_paragraph_style(self):
        assert ParagraphStyleType.Title.group_identifier() == 0
        assert ParagraphStyleType.Heading.group_identifier() == 1
        assert ParagraphStyleType.Subheading.group_identifier() == 2
        assert ParagraphStyleType.CodeBlock.group_identifier() == 4
        assert ParagraphStyleType.DotList.group_identifier() == 100
        assert ParagraphStyleType.DashList.group_identifier() == 100
        assert ParagraphStyleType.NumberList.group_identifier() == 100
        assert ParagraphStyleType.TodoList.group_identifier() == 100

    def test_paragraph_is_same_paragraph(self):
        empty = ParagraphStyle()
        title = ParagraphStyle(style_type=ParagraphStyleType.Title)
        heading = ParagraphStyle(style_type=ParagraphStyleType.Heading)
        subheading = ParagraphStyle(style_type=ParagraphStyleType.Subheading)
        code_block = ParagraphStyle(style_type=ParagraphStyleType.CodeBlock)
        dot_list = ParagraphStyle(style_type=ParagraphStyleType.DotList)
        dash_list = ParagraphStyle(style_type=ParagraphStyleType.DashList)
        number_list = ParagraphStyle(style_type=ParagraphStyleType.NumberList)
        todo_list = ParagraphStyle(style_type=ParagraphStyleType.TodoList)
        
        assert empty.is_same_block(empty)
        assert empty.is_same_block(title)
        assert empty.is_same_block(heading)
        assert empty.is_same_block(subheading)
        assert empty.is_same_block(code_block)
        assert empty.is_same_block(dot_list)
        assert empty.is_same_block(dash_list)
        assert empty.is_same_block(number_list)
        assert empty.is_same_block(todo_list)

        assert title.is_same_block(empty)
        assert title.is_same_block(title)
        assert not title.is_same_block(heading)
        assert not title.is_same_block(subheading)
        assert not title.is_same_block(code_block)
        assert not title.is_same_block(dot_list)
        assert not title.is_same_block(dash_list)
        assert not title.is_same_block(number_list)
        assert not title.is_same_block(todo_list)
        
        assert heading.is_same_block(empty)
        assert heading.is_same_block(title)
        assert heading.is_same_block(heading)
        assert not heading.is_same_block(subheading)
        assert not heading.is_same_block(code_block)
        assert not heading.is_same_block(dot_list)
        assert not heading.is_same_block(dash_list)
        assert not heading.is_same_block(number_list)
        assert not heading.is_same_block(todo_list)

        assert subheading.is_same_block(empty)
        assert subheading.is_same_block(title)
        assert subheading.is_same_block(heading)
        assert subheading.is_same_block(subheading)
        assert not subheading.is_same_block(code_block)
        assert not subheading.is_same_block(dot_list)
        assert not subheading.is_same_block(dash_list)
        assert not subheading.is_same_block(number_list)
        assert not subheading.is_same_block(todo_list)

        assert code_block.is_same_block(empty)
        assert code_block.is_same_block(title)
        assert code_block.is_same_block(heading)
        assert code_block.is_same_block(subheading)
        assert code_block.is_same_block(code_block)
        assert not code_block.is_same_block(dot_list)
        assert not code_block.is_same_block(dash_list)
        assert not code_block.is_same_block(number_list)
        assert not code_block.is_same_block(todo_list)

        assert dot_list.is_same_block(empty)
        assert dot_list.is_same_block(title)
        assert dot_list.is_same_block(heading)
        assert dot_list.is_same_block(subheading)
        assert dot_list.is_same_block(code_block)
        assert dot_list.is_same_block(dot_list)
        assert dot_list.is_same_block(dash_list)
        assert dot_list.is_same_block(number_list)
        assert dot_list.is_same_block(todo_list)

        assert dash_list.is_same_block(empty)
        assert dash_list.is_same_block(title)
        assert dash_list.is_same_block(heading)
        assert dash_list.is_same_block(subheading)
        assert dash_list.is_same_block(code_block)
        assert dash_list.is_same_block(dot_list)
        assert dash_list.is_same_block(dash_list)
        assert dash_list.is_same_block(number_list)
        assert dash_list.is_same_block(todo_list)

        assert number_list.is_same_block(empty)
        assert number_list.is_same_block(title)
        assert number_list.is_same_block(heading)
        assert number_list.is_same_block(subheading)
        assert number_list.is_same_block(code_block)
        assert number_list.is_same_block(dot_list)
        assert number_list.is_same_block(dash_list)
        assert number_list.is_same_block(number_list)
        assert number_list.is_same_block(todo_list)

        assert todo_list.is_same_block(empty)
        assert todo_list.is_same_block(title)
        assert todo_list.is_same_block(heading)
        assert todo_list.is_same_block(subheading)
        assert todo_list.is_same_block(code_block)
        assert todo_list.is_same_block(dot_list)
        assert todo_list.is_same_block(dash_list)
        assert todo_list.is_same_block(number_list)
        assert todo_list.is_same_block(todo_list)

    def test_quote_is_same_paragraph(self):
        empty = ParagraphStyle(quote=False)
        quote = ParagraphStyle(quote=True)

        assert not quote.is_same_block(empty)
        assert quote.is_same_block(quote)
        assert not empty.is_same_block(quote)
        assert empty.is_same_block(empty)

    def test_check_info_is_same_paragraph(self):
        check = ParagraphStyle(check_info=CheckInfo(done=False, uuid="uuid"))

        assert check.is_same_block(check)
