from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Color(_message.Message):
    __slots__ = ("red", "green", "blue", "alpha")
    RED_FIELD_NUMBER: _ClassVar[int]
    GREEN_FIELD_NUMBER: _ClassVar[int]
    BLUE_FIELD_NUMBER: _ClassVar[int]
    ALPHA_FIELD_NUMBER: _ClassVar[int]
    red: float
    green: float
    blue: float
    alpha: float
    def __init__(self, red: _Optional[float] = ..., green: _Optional[float] = ..., blue: _Optional[float] = ..., alpha: _Optional[float] = ...) -> None: ...

class AttachmentInfo(_message.Message):
    __slots__ = ("attachment_identifier", "type_uti")
    ATTACHMENT_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    TYPE_UTI_FIELD_NUMBER: _ClassVar[int]
    attachment_identifier: str
    type_uti: str
    def __init__(self, attachment_identifier: _Optional[str] = ..., type_uti: _Optional[str] = ...) -> None: ...

class Font(_message.Message):
    __slots__ = ("font_name", "point_size", "font_hints")
    FONT_NAME_FIELD_NUMBER: _ClassVar[int]
    POINT_SIZE_FIELD_NUMBER: _ClassVar[int]
    FONT_HINTS_FIELD_NUMBER: _ClassVar[int]
    font_name: str
    point_size: float
    font_hints: int
    def __init__(self, font_name: _Optional[str] = ..., point_size: _Optional[float] = ..., font_hints: _Optional[int] = ...) -> None: ...

class ParagraphStyle(_message.Message):
    __slots__ = ("style_type", "alignment", "indent_amount", "checklist", "block_quote")
    STYLE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    INDENT_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    CHECKLIST_FIELD_NUMBER: _ClassVar[int]
    BLOCK_QUOTE_FIELD_NUMBER: _ClassVar[int]
    style_type: int
    alignment: int
    indent_amount: int
    checklist: Checklist
    block_quote: int
    def __init__(self, style_type: _Optional[int] = ..., alignment: _Optional[int] = ..., indent_amount: _Optional[int] = ..., checklist: _Optional[_Union[Checklist, _Mapping]] = ..., block_quote: _Optional[int] = ...) -> None: ...

class Checklist(_message.Message):
    __slots__ = ("uuid", "done")
    UUID_FIELD_NUMBER: _ClassVar[int]
    DONE_FIELD_NUMBER: _ClassVar[int]
    uuid: bytes
    done: int
    def __init__(self, uuid: _Optional[bytes] = ..., done: _Optional[int] = ...) -> None: ...

class DictionaryElement(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: ObjectID
    value: ObjectID
    def __init__(self, key: _Optional[_Union[ObjectID, _Mapping]] = ..., value: _Optional[_Union[ObjectID, _Mapping]] = ...) -> None: ...

class Dictionary(_message.Message):
    __slots__ = ("element",)
    ELEMENT_FIELD_NUMBER: _ClassVar[int]
    element: _containers.RepeatedCompositeFieldContainer[DictionaryElement]
    def __init__(self, element: _Optional[_Iterable[_Union[DictionaryElement, _Mapping]]] = ...) -> None: ...

class ObjectID(_message.Message):
    __slots__ = ("unsigned_integer_value", "string_value", "object_index")
    UNSIGNED_INTEGER_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_INDEX_FIELD_NUMBER: _ClassVar[int]
    unsigned_integer_value: int
    string_value: str
    object_index: int
    def __init__(self, unsigned_integer_value: _Optional[int] = ..., string_value: _Optional[str] = ..., object_index: _Optional[int] = ...) -> None: ...

class RegisterLatest(_message.Message):
    __slots__ = ("contents",)
    CONTENTS_FIELD_NUMBER: _ClassVar[int]
    contents: ObjectID
    def __init__(self, contents: _Optional[_Union[ObjectID, _Mapping]] = ...) -> None: ...

class MapEntry(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: int
    value: ObjectID
    def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[ObjectID, _Mapping]] = ...) -> None: ...

class AttributeRun(_message.Message):
    __slots__ = ("length", "paragraph_style", "font", "font_weight", "underlined", "strikethrough", "superscript", "link", "color", "attachment_info")
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    PARAGRAPH_STYLE_FIELD_NUMBER: _ClassVar[int]
    FONT_FIELD_NUMBER: _ClassVar[int]
    FONT_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    UNDERLINED_FIELD_NUMBER: _ClassVar[int]
    STRIKETHROUGH_FIELD_NUMBER: _ClassVar[int]
    SUPERSCRIPT_FIELD_NUMBER: _ClassVar[int]
    LINK_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENT_INFO_FIELD_NUMBER: _ClassVar[int]
    length: int
    paragraph_style: ParagraphStyle
    font: Font
    font_weight: int
    underlined: int
    strikethrough: int
    superscript: int
    link: str
    color: Color
    attachment_info: AttachmentInfo
    def __init__(self, length: _Optional[int] = ..., paragraph_style: _Optional[_Union[ParagraphStyle, _Mapping]] = ..., font: _Optional[_Union[Font, _Mapping]] = ..., font_weight: _Optional[int] = ..., underlined: _Optional[int] = ..., strikethrough: _Optional[int] = ..., superscript: _Optional[int] = ..., link: _Optional[str] = ..., color: _Optional[_Union[Color, _Mapping]] = ..., attachment_info: _Optional[_Union[AttachmentInfo, _Mapping]] = ...) -> None: ...

class NoteStoreProto(_message.Message):
    __slots__ = ("document",)
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    document: Document
    def __init__(self, document: _Optional[_Union[Document, _Mapping]] = ...) -> None: ...

class Document(_message.Message):
    __slots__ = ("version", "note")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    version: int
    note: Note
    def __init__(self, version: _Optional[int] = ..., note: _Optional[_Union[Note, _Mapping]] = ...) -> None: ...

class Note(_message.Message):
    __slots__ = ("note_text", "attribute_run")
    NOTE_TEXT_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_RUN_FIELD_NUMBER: _ClassVar[int]
    note_text: str
    attribute_run: _containers.RepeatedCompositeFieldContainer[AttributeRun]
    def __init__(self, note_text: _Optional[str] = ..., attribute_run: _Optional[_Iterable[_Union[AttributeRun, _Mapping]]] = ...) -> None: ...

class MergableDataProto(_message.Message):
    __slots__ = ("mergable_data_object",)
    MERGABLE_DATA_OBJECT_FIELD_NUMBER: _ClassVar[int]
    mergable_data_object: MergableDataObject
    def __init__(self, mergable_data_object: _Optional[_Union[MergableDataObject, _Mapping]] = ...) -> None: ...

class MergableDataObject(_message.Message):
    __slots__ = ("version", "mergeable_data_object_data")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    MERGEABLE_DATA_OBJECT_DATA_FIELD_NUMBER: _ClassVar[int]
    version: int
    mergeable_data_object_data: MergeableDataObjectData
    def __init__(self, version: _Optional[int] = ..., mergeable_data_object_data: _Optional[_Union[MergeableDataObjectData, _Mapping]] = ...) -> None: ...

class MergeableDataObjectData(_message.Message):
    __slots__ = ("mergeable_data_object_entry", "mergeable_data_object_key_item", "mergeable_data_object_type_item", "mergeable_data_object_uuid_item")
    MERGEABLE_DATA_OBJECT_ENTRY_FIELD_NUMBER: _ClassVar[int]
    MERGEABLE_DATA_OBJECT_KEY_ITEM_FIELD_NUMBER: _ClassVar[int]
    MERGEABLE_DATA_OBJECT_TYPE_ITEM_FIELD_NUMBER: _ClassVar[int]
    MERGEABLE_DATA_OBJECT_UUID_ITEM_FIELD_NUMBER: _ClassVar[int]
    mergeable_data_object_entry: _containers.RepeatedCompositeFieldContainer[MergeableDataObjectEntry]
    mergeable_data_object_key_item: _containers.RepeatedScalarFieldContainer[str]
    mergeable_data_object_type_item: _containers.RepeatedScalarFieldContainer[str]
    mergeable_data_object_uuid_item: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, mergeable_data_object_entry: _Optional[_Iterable[_Union[MergeableDataObjectEntry, _Mapping]]] = ..., mergeable_data_object_key_item: _Optional[_Iterable[str]] = ..., mergeable_data_object_type_item: _Optional[_Iterable[str]] = ..., mergeable_data_object_uuid_item: _Optional[_Iterable[bytes]] = ...) -> None: ...

class MergeableDataObjectEntry(_message.Message):
    __slots__ = ("register_latest", "list", "dictionary", "unknown_message", "note", "custom_map", "ordered_set")
    REGISTER_LATEST_FIELD_NUMBER: _ClassVar[int]
    LIST_FIELD_NUMBER: _ClassVar[int]
    DICTIONARY_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_MAP_FIELD_NUMBER: _ClassVar[int]
    ORDERED_SET_FIELD_NUMBER: _ClassVar[int]
    register_latest: RegisterLatest
    list: List
    dictionary: Dictionary
    unknown_message: UnknownMergeableDataObjectEntryMessage
    note: Note
    custom_map: MergeableDataObjectMap
    ordered_set: OrderedSet
    def __init__(self, register_latest: _Optional[_Union[RegisterLatest, _Mapping]] = ..., list: _Optional[_Union[List, _Mapping]] = ..., dictionary: _Optional[_Union[Dictionary, _Mapping]] = ..., unknown_message: _Optional[_Union[UnknownMergeableDataObjectEntryMessage, _Mapping]] = ..., note: _Optional[_Union[Note, _Mapping]] = ..., custom_map: _Optional[_Union[MergeableDataObjectMap, _Mapping]] = ..., ordered_set: _Optional[_Union[OrderedSet, _Mapping]] = ...) -> None: ...

class UnknownMergeableDataObjectEntryMessage(_message.Message):
    __slots__ = ("unknown_entry",)
    UNKNOWN_ENTRY_FIELD_NUMBER: _ClassVar[int]
    unknown_entry: UnknownMergeableDataObjectEntryMessageEntry
    def __init__(self, unknown_entry: _Optional[_Union[UnknownMergeableDataObjectEntryMessageEntry, _Mapping]] = ...) -> None: ...

class UnknownMergeableDataObjectEntryMessageEntry(_message.Message):
    __slots__ = ("unknown_int1", "unknown_int2")
    UNKNOWN_INT1_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_INT2_FIELD_NUMBER: _ClassVar[int]
    unknown_int1: int
    unknown_int2: int
    def __init__(self, unknown_int1: _Optional[int] = ..., unknown_int2: _Optional[int] = ...) -> None: ...

class MergeableDataObjectMap(_message.Message):
    __slots__ = ("type", "map_entry")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MAP_ENTRY_FIELD_NUMBER: _ClassVar[int]
    type: int
    map_entry: _containers.RepeatedCompositeFieldContainer[MapEntry]
    def __init__(self, type: _Optional[int] = ..., map_entry: _Optional[_Iterable[_Union[MapEntry, _Mapping]]] = ...) -> None: ...

class OrderedSet(_message.Message):
    __slots__ = ("ordering", "elements")
    ORDERING_FIELD_NUMBER: _ClassVar[int]
    ELEMENTS_FIELD_NUMBER: _ClassVar[int]
    ordering: OrderedSetOrdering
    elements: Dictionary
    def __init__(self, ordering: _Optional[_Union[OrderedSetOrdering, _Mapping]] = ..., elements: _Optional[_Union[Dictionary, _Mapping]] = ...) -> None: ...

class OrderedSetOrdering(_message.Message):
    __slots__ = ("array", "contents")
    ARRAY_FIELD_NUMBER: _ClassVar[int]
    CONTENTS_FIELD_NUMBER: _ClassVar[int]
    array: OrderedSetOrderingArray
    contents: Dictionary
    def __init__(self, array: _Optional[_Union[OrderedSetOrderingArray, _Mapping]] = ..., contents: _Optional[_Union[Dictionary, _Mapping]] = ...) -> None: ...

class OrderedSetOrderingArray(_message.Message):
    __slots__ = ("contents", "attachment")
    CONTENTS_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENT_FIELD_NUMBER: _ClassVar[int]
    contents: Note
    attachment: _containers.RepeatedCompositeFieldContainer[OrderedSetOrderingArrayAttachment]
    def __init__(self, contents: _Optional[_Union[Note, _Mapping]] = ..., attachment: _Optional[_Iterable[_Union[OrderedSetOrderingArrayAttachment, _Mapping]]] = ...) -> None: ...

class OrderedSetOrderingArrayAttachment(_message.Message):
    __slots__ = ("index", "uuid")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    index: int
    uuid: bytes
    def __init__(self, index: _Optional[int] = ..., uuid: _Optional[bytes] = ...) -> None: ...

class List(_message.Message):
    __slots__ = ("list_entry",)
    LIST_ENTRY_FIELD_NUMBER: _ClassVar[int]
    list_entry: _containers.RepeatedCompositeFieldContainer[ListEntry]
    def __init__(self, list_entry: _Optional[_Iterable[_Union[ListEntry, _Mapping]]] = ...) -> None: ...

class ListEntry(_message.Message):
    __slots__ = ("id", "details", "additional_details")
    ID_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_DETAILS_FIELD_NUMBER: _ClassVar[int]
    id: ObjectID
    details: ListEntryDetails
    additional_details: ListEntryDetails
    def __init__(self, id: _Optional[_Union[ObjectID, _Mapping]] = ..., details: _Optional[_Union[ListEntryDetails, _Mapping]] = ..., additional_details: _Optional[_Union[ListEntryDetails, _Mapping]] = ...) -> None: ...

class ListEntryDetails(_message.Message):
    __slots__ = ("list_entry_details_key", "id")
    LIST_ENTRY_DETAILS_KEY_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    list_entry_details_key: ListEntryDetailsKey
    id: ObjectID
    def __init__(self, list_entry_details_key: _Optional[_Union[ListEntryDetailsKey, _Mapping]] = ..., id: _Optional[_Union[ObjectID, _Mapping]] = ...) -> None: ...

class ListEntryDetailsKey(_message.Message):
    __slots__ = ("list_entry_details_type_index", "list_entry_details_key")
    LIST_ENTRY_DETAILS_TYPE_INDEX_FIELD_NUMBER: _ClassVar[int]
    LIST_ENTRY_DETAILS_KEY_FIELD_NUMBER: _ClassVar[int]
    list_entry_details_type_index: int
    list_entry_details_key: int
    def __init__(self, list_entry_details_type_index: _Optional[int] = ..., list_entry_details_key: _Optional[int] = ...) -> None: ...
