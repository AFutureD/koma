from pathlib import Path
import unittest

from koma.domain.models.attachment import NoteAttachment
from koma.domain.models.style import AttributeText, FontStyle, TextAttribute
from koma.infra.renderers.markdown import MarkDown


class RenderMarkdownTests(unittest.TestCase):
    
    markdown = MarkDown()

    def test_render_link(self):
    
        model = NoteAttachment(
            type_uti="public.url",
            z_pk=1,
            identifier="fake_identifier",
            note_pk=1,
            text="Google",
            parent_pk=None,
            url="https://www.google.com"
        )
        result = self.markdown.render_attachment_link(model)
        assert result == "[Google](https://www.google.com)"

    def test_render_media(self):
    
        model_1 = NoteAttachment(
            type_uti="public.any",
            z_pk=1,
            identifier="fake_identifier",
            note_pk=1,
            text="Google",
            parent_pk=None,
            media_root_path="fake_path",
            generation="fake_generation",
            file_uuid="fake_uuid",
            file_name="fake_name",
        )
        result_1 = self.markdown.render_attachment_media(model_1)
        assert result_1 == "![Google](fake_path/Media/fake_uuid/fake_generation/fake_name)"

        model_2 = NoteAttachment(
            type_uti="public.any",
            z_pk=1,
            identifier="fake_identifier",
            note_pk=1,
            text="Google",
            parent_pk=None,
            media_root_path="fake_path",
            generation=None,
            file_uuid="fake_uuid",
            file_name="fake_name",
        )
        result_2 = self.markdown.render_attachment_media(model_2)
        assert result_2 == "![Google](fake_path/Media/fake_uuid/fake_name)"

    def test_render_tag(self):
    
        model = NoteAttachment(
            type_uti="com.apple.notes.inlinetextattachment.hashtag",
            z_pk=1,
            identifier="fake_identifier",
            note_pk=1,
            text="#Google",
            parent_pk=None
        )
        result = self.markdown.render_attachment_tag(model)
        assert result == "#Google"
    
    def test_render_draw(self):
    
        model_1 = NoteAttachment(
            type_uti="com.apple.drawing",
            z_pk=1,
            identifier="fake_identifier",
            note_pk=1,
            text="Google",
            parent_pk=None,
            media_root_path="fake_path",
            generation="fake_generation",
            file_uuid="fake_uuid",
            file_name="fake_name",
        )
        result_1: str = self.markdown.render_attachment_draw(model_1)
        assert result_1 == "[Google](fake_path/FallbackImages/fake_identifier/fake_generation/FallbackImage.png)"

        model_2 = NoteAttachment(
            type_uti="com.apple.drawing",
            z_pk=1,
            identifier="fake_identifier",
            note_pk=1,
            text="Google",
            parent_pk=None,
            media_root_path="fake_path",
            generation=None,
            file_uuid="fake_uuid",
            file_name="fake_name",
        )
        result_2 = self.markdown.render_attachment_draw(model_2)
        assert result_2 == "[Google](fake_path/FallbackImages/fake_identifier.jpg)"

    def test_render_table(self):
    
        model = NoteAttachment(
            type_uti="com.apple.notes.table",
            z_pk=1,
            identifier="fake_identifier",
            note_pk=1,
            text="Google",
            parent_pk=None,
            table_cell_list=[]
        )
        result = self.markdown.render_attachment_table(model)
        assert result == ""
    
    def test_render_gallery(self):
    
        model = NoteAttachment(
            type_uti="com.apple.notes.gallery",
            z_pk=1,
            identifier="fake_identifier",
            note_pk=1,
            text="Google",
            parent_pk=None
        )
        result = self.markdown.render_attachment_gallery(model)
        assert result == ""

    def test_render_text(self):
        
        text_1 = AttributeText(start_index=0,length=1,text="a",attribute=TextAttribute())
        result_1 = self.markdown.render_attribute_text(text_1)
        assert result_1 == "a"

        text_2 = AttributeText(start_index=0,length=1,text="a",attribute=TextAttribute(font_style=FontStyle.Bold))
        result_2 = self.markdown.render_attribute_text(text_2)
        assert result_2 == "**a**"

        text_3 = AttributeText(start_index=0,length=1,text="a",attribute=TextAttribute(font_style=FontStyle.Italic))
        result_3 = self.markdown.render_attribute_text(text_3)
        assert result_3 == "*a*"

        text_4 = AttributeText(start_index=0,length=1,text="a",attribute=TextAttribute(font_style=FontStyle.Bold_Italic))
        result_4 = self.markdown.render_attribute_text(text_4)
        assert result_4 == "***a***"

        text_5 = AttributeText(start_index=0,length=1,text="a",attribute=TextAttribute(font_style=FontStyle.Bold, link="https://www.google.com"))
        result_5 = self.markdown.render_attribute_text(text_5)
        assert result_5 == "[**a**](https://www.google.com)"

        text_6 = AttributeText(start_index=0,length=1,text="a",attribute=TextAttribute(font_style=FontStyle.Bold, strike_through=True))
        result_6 = self.markdown.render_attribute_text(text_6)
        assert result_6 == "~~**a**~~"
