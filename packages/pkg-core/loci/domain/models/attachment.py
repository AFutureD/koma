from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Protocol

from pydantic import BaseModel, ConfigDict
from pydantic._internal._model_construction import ModelMetaclass

from ...core import RenderAble, Model


class NoteAttachmentTableCell(Model):
    column: int
    row: int
    text: str

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "NoteAttachmentTableCell(column: {}, row: {}, text: {})".format(self.column, self.row, self.text)


class NoteAttachmentFactory(ModelMetaclass):

    def __call__(cls, *args, **kwargs):
        type_uti = kwargs.get("type_uti")
        if type_uti == "public.url":
            return NoteAttachmentLink(**kwargs)
        elif type_uti in ["com.apple.paper", "com.apple.drawing.2", "com.apple.drawing"]:
            return NoteAttachmentDraw(**kwargs)
        elif type_uti in ["com.apple.notes.table"]:
            return NoteAttachmentTable(**kwargs)
        elif type_uti in ["com.apple.notes.inlinetextattachment.hashtag"]:
            return NoteAttachmentTag(**kwargs)
        elif type_uti == "com.apple.notes.gallery":
            return NoteAttachmentGallery(**kwargs)
        else:
            return NoteAttachmentMedia(**kwargs)


class NoteAttachmentMetaClass(NoteAttachmentFactory):

    def __call__(cls, *args, **kwargs):
        return type.__call__(cls, *args, **kwargs)


class NoteAttachment(RenderAble, Model, metaclass=NoteAttachmentFactory):

    type_uti: str
    z_pk: int
    identifier: str
    note_pk: int
    text: None | str
    parent_pk: None | int
    _children: Dict[str, NoteAttachment] = {}

    def __hash__(self):
        return hash((self.identifier, self.type_uti))

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.__class__.__name__}(identifier: {self.identifier}, type_uti: {self.type_uti}, z_pk: {self.z_pk}, note_pk: {self.note_pk}, parent_pk: {self.parent_pk})"

    def append_children(self, attachments: List[NoteAttachment]):
        for attachment in attachments:
            self.append_child(attachment)

    def append_child(self, attachment: NoteAttachment):
        self._children[attachment.identifier] = attachment

    def get_child(self, identifier: str) -> None | NoteAttachment:
        return self._children.get(identifier)

    def get_data_path(self) -> None | str:
        return None


class NoteAttachmentLink(NoteAttachment, metaclass=NoteAttachmentMetaClass):

    url: str


class NoteAttachmentMedia(NoteAttachment, metaclass=NoteAttachmentMetaClass):
    generation: None | str
    media_root_path: str
    file_uuid: str
    file_name: str

    def get_data_path(self) -> str:
        
        if self.generation is None:
            data_path = f"Media/{self.file_uuid}/{self.file_name}"
        else:
            data_path = f"Media/{self.file_uuid}/{self.generation}/{self.file_name}"

        return f"{self.media_root_path}/{data_path}"


class NoteAttachmentDraw(NoteAttachment, metaclass=NoteAttachmentMetaClass):
    generation: None | str
    media_root_path: str

    def get_data_path(self) -> str:

        if self.generation is None:
            data_path = f"FallbackImages/{self.identifier}.jpg"
        else:
            data_path = f"FallbackImages/{self.identifier}/{self.generation}/FallbackImage.png"

        return f"{self.media_root_path}/{data_path}"


class NoteAttachmentTable(NoteAttachment, metaclass=NoteAttachmentMetaClass):
    model_config = ConfigDict(arbitrary_types_allowed = True)

    table_cell_list: List[NoteAttachmentTableCell]


class NoteAttachmentTag(NoteAttachment, metaclass=NoteAttachmentMetaClass):
    pass


class NoteAttachmentGallery(NoteAttachment, metaclass=NoteAttachmentMetaClass):
    pass
