import logging
from pathlib import Path

from koma.core.render import RenderAble
from ..renderers.base import Renderer
from ...domain import Note, NoteContent, NoteContentParagraph, NoteContentLine, AttributeText, NoteAttachmentLink, NoteAttachmentMedia, NoteAttachmentTag, NoteAttachmentDraw, NoteAttachmentTable, NoteAttachmentGallery, ParagraphStyleType, FontStyle

logger = logging.getLogger(__name__)


class MarkDown(Renderer):

    def post_render(self, render_able: RenderAble):
        # logger.debug(f"Rendered: {render_able.represent.__repr__()}")
        pass

    def render_attachment_link(self, attachment: NoteAttachmentLink) -> str:
        return f"[{attachment.text}]({attachment.url})"

    def render_attachment_media(self, attachment: NoteAttachmentMedia) -> str:
        media_path = attachment.get_data_path()
        text = attachment.text
        if text is None and media_path is not None:
            return ""
        elif text is not None and media_path is None:
            return f"![{text}]()"
        elif text is None and media_path is not None:
            return f"![]({media_path})"
        else:
            return f"![{text}]({media_path})"

    def render_attachment_tag(self, attachment: NoteAttachmentTag) -> str:
        return attachment.text if attachment.text is not None else ""

    def render_attachment_draw(self, attachment: NoteAttachmentDraw) -> str:
        media_path = attachment.get_data_path()
        return f"[{attachment.text}]({media_path})"

    def render_attachment_table(self, attribute: NoteAttachmentTable) -> str:
        # TODO: Implement table rendering
        return ""

    def render_attachment_gallery(self, attribute: NoteAttachmentGallery) -> str:
        # TODO: Implement gallery rendering
        return ""

    def render_attribute_text(self, attribute_text: AttributeText) -> str:
        attribute = attribute_text.attribute

        if attribute is None:
            return attribute_text.text

        if attribute.attachment:
            represent = attribute.attachment.rendered_result
            return represent if represent is not None else ""

        markdown_text = attribute_text.text

        if attribute.font_style is not None:
            font_style = attribute.font_style
            if font_style == FontStyle.Bold:
                markdown_text = f"**{markdown_text}**"
            elif font_style == FontStyle.Italic:
                markdown_text = f"*{markdown_text}*"
            elif font_style == FontStyle.Bold_Italic:
                markdown_text = f"***{markdown_text}***"

        if attribute.link:
            return f"[{markdown_text}]({attribute.link})"

        if attribute.strike_through:
            return f"~~{markdown_text}~~"

        return markdown_text

    def render_line(self, line: NoteContentLine) -> str:

        markdown_text = "".join([
            ele.rendered_result
            for ele in line.elements
            if ele.rendered_result is not None
        ])

        return markdown_text

    def render_paragraph(self, paragraph: NoteContentParagraph) -> str:
        attribute = paragraph.attribute

        markdown_text = "".join([
            line.rendered_result
            for line in paragraph.lines
            if line.rendered_result is not None
        ])

        if attribute is None:
            return markdown_text

        # code block
        if attribute.style_type is not None and attribute.style_type == ParagraphStyleType.CodeBlock:
            return f"```\n{markdown_text}```\n"

        markdown_text = ""
        number_list_stack = []
        previous_indent = -1
        for line in paragraph.lines:
            # if line.is_paragraph_breaker():
            #     continue

            markdown_line = line.rendered_result
            line_attribute = line.attribute

            if markdown_line is None:
                continue

            if line_attribute is None:
                markdown_text += markdown_line
                continue

            indent = line_attribute.indent_level * 2
            prefix = " " * indent

            if line_attribute.quote is not None and line_attribute.quote:
                markdown_text += f"> {prefix}{markdown_line}"
            elif line_attribute.check_info is not None:
                done = line_attribute.check_info.done
                markdown_text += prefix + f"- [{"x" if done else " "}] {markdown_line}"
            elif line_attribute.style_type is not None:
                style = line_attribute.style_type
                if style == ParagraphStyleType.Title:
                    markdown_text += prefix + f"# {markdown_line}"
                elif style == ParagraphStyleType.Heading:
                    markdown_text += prefix + f"## {markdown_line}"
                elif style == ParagraphStyleType.Subheading:
                    markdown_text += prefix + f"### {markdown_line}"
                elif style == ParagraphStyleType.DotList:
                    markdown_text += prefix + f"* {markdown_line}"
                elif style == ParagraphStyleType.DashList:
                    markdown_text += prefix + f"- {markdown_line}"
                elif style == ParagraphStyleType.NumberList:
                    if indent > previous_indent:
                        the_number = 1
                        number_list_stack.append(the_number)
                    elif indent < previous_indent:
                        number_list_stack.pop()
                        the_number = number_list_stack[-1]
                        the_number += 1
                        number_list_stack[-1] = the_number
                    else:
                        the_number = number_list_stack[-1]
                        the_number += 1
                        number_list_stack[-1] = the_number

                    markdown_text += prefix + f"{the_number:2}. {markdown_line}"
                    previous_indent = indent
            else:
                markdown_text += markdown_line

        logger.debug(f"paragraph: {markdown_text.__repr__()}")
        return markdown_text

    def render_content(self, content: NoteContent) -> str:
        return "".join([
            paragraph.rendered_result
            for paragraph in content.paragraph_list
            if paragraph.rendered_result is not None
        ])

    def render_memory(self, memory: Note) -> str:
        re = memory.content.rendered_result
        return re if re is not None else ""
