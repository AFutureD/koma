from __future__ import annotations
from abc import ABCMeta, abstractmethod

# if TYPE_CHECKING:
from ...domain import Note, NoteContent, NoteContentParagraph, NoteContentLine, AttributeText, NoteAttachmentLink, NoteAttachmentMedia, NoteAttachmentTag, NoteAttachmentDraw, NoteAttachmentTable, NoteAttachmentGallery
from ...core import RenderAble, TextRenderer, Model


class Renderer(TextRenderer, Model, metaclass=ABCMeta):

    def pre_render(self, render_able: RenderAble):
        pass

    def post_render(self, render_able: RenderAble):
        pass

    def render_attachment_link(self, attachment: NoteAttachmentLink) -> str:
        return ""

    def render_attachment_media(self, attachment: NoteAttachmentMedia) -> str:
        return ""

    def render_attachment_tag(self, attachment: NoteAttachmentTag) -> str:
        return ""

    def render_attachment_draw(self, attachment: NoteAttachmentDraw) -> str:
        return ""

    def render_attachment_table(self, attribute: NoteAttachmentTable) -> str:
        return ""

    def render_attachment_gallery(self, attribute: NoteAttachmentGallery) -> str:
        return ""

    @abstractmethod
    def render_attribute_text(self, attribute: AttributeText) -> str:
        ...

    @abstractmethod
    def render_line(self, line: NoteContentLine) -> str:
        ...

    @abstractmethod
    def render_paragraph(self, paragraph: NoteContentParagraph) -> str:
        ...

    @abstractmethod
    def render_content(self, content: NoteContent) -> str:
        ...

    @abstractmethod
    def render_memory(self, memory: Note) -> str:
        ...

    def render(self, render_able: RenderAble):
        if isinstance(render_able, Note):
            return self.render_memory(render_able)
        elif isinstance(render_able, NoteContent):
            return self.render_content(render_able)
        elif isinstance(render_able, NoteContentParagraph):
            return self.render_paragraph(render_able)
        elif isinstance(render_able, NoteContentLine):
            return self.render_line(render_able)
        elif isinstance(render_able, AttributeText):
            return self.render_attribute_text(render_able)
        elif isinstance(render_able, NoteAttachmentLink):
            return self.render_attachment_link(render_able)
        elif isinstance(render_able, NoteAttachmentMedia):
            return self.render_attachment_media(render_able)
        elif isinstance(render_able, NoteAttachmentTag):
            return self.render_attachment_tag(render_able)
        elif isinstance(render_able, NoteAttachmentDraw):
            return self.render_attachment_draw(render_able)
        elif isinstance(render_able, NoteAttachmentTable):
            return self.render_attachment_table(render_able)
        elif isinstance(render_able, NoteAttachmentGallery):
            return self.render_attachment_gallery(render_able)
        else:
            raise RuntimeError(f"Unknown type {type(self)}")

