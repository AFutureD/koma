import itertools
from typing import Dict, List, Sequence

from ...domain import (
    AttributeText,
    CheckInfo,
    FontStyle,
    NoteAttachmentTableCell,
    NoteContentLine,
    NoteContentParagraph,
    ParagraphStyle,
    ParagraphStyleType,
    TextAttribute,
)
from ...protobuf import (
    AttributeRun,
    Checklist,
    DictionaryElement,
    MergableDataProto,
    MergeableDataObjectEntry,
    MergeableDataObjectMap,
    ParagraphStyle_pb2,
)


def build_check(check: Checklist) -> None | CheckInfo:
    if check.uuid == b'':
        return None
    return CheckInfo(done = (check.done == 1), uuid = check.uuid.hex())


def build_note_attribute(attribute_run: AttributeRun) -> TextAttribute:

    paragraph_style: None | ParagraphStyle = None
    font_style: None | FontStyle = None
    font: None | str = None
    underlined: None | bool = None
    strike_through: None | bool = None
    attachment_identifier: None | str = None
    link: None | str = None

    if attribute_run.HasField("paragraph_style"):
        paragraph_style = build_note_paragraph_style(attribute_run.paragraph_style)
    if attribute_run.HasField("font"):
        font = attribute_run.font.font_name
    if attribute_run.HasField("font_weight"):
        font_style = FontStyle(attribute_run.font_weight)
    if attribute_run.HasField("underlined"):
        underlined = attribute_run.underlined == 1
    if attribute_run.HasField("strikethrough"):
        strike_through = attribute_run.strikethrough == 1
    if attribute_run.HasField("attachment_info"):
        info = attribute_run.attachment_info
        attachment_identifier = info.attachment_identifier
    if attribute_run.HasField("link"):
        link = attribute_run.link

    return TextAttribute(
        paragraph_style = paragraph_style,
        font_style = font_style,
        font_name = font,
        underlined = underlined,
        strike_through = strike_through,
        link = link,
        attachment_identifier = attachment_identifier,
    )


def build_note_paragraph_style(paragraph_style: ParagraphStyle_pb2) -> ParagraphStyle:
    style_type: None | ParagraphStyleType = None
    indent_amount = 0
    check_info: None | CheckInfo = None
    is_quote: bool = False

    if paragraph_style.HasField("checklist"):
        check_info = build_check(paragraph_style.checklist)
    if paragraph_style.HasField("style_type"):
        style_type = ParagraphStyleType(paragraph_style.style_type)
    if paragraph_style.HasField("indent_amount"):
        indent_amount = paragraph_style.indent_amount
    if paragraph_style.HasField("block_quote"):
        is_quote = paragraph_style.block_quote == 1

    return ParagraphStyle(style_type = style_type, indent_level = indent_amount, check_info = check_info, quote = is_quote)


def build_content_lines(attribute_text_list: Sequence[AttributeText]) -> List[NoteContentLine]:
    split_list = [attribute.splitlines() for attribute in attribute_text_list]
    flatten_text_list = list(itertools.chain.from_iterable(split_list))

    # build a line.
    lines: List[NoteContentLine] = []

    line_idx = 0
    one_line_stack: List[AttributeText] = []
    for idx, text_attribute in enumerate(flatten_text_list):
        if text_attribute is None:
            continue
        one_line_stack.append(text_attribute)
        if "\n" not in text_attribute.text and idx != len(flatten_text_list) - 1:
            continue

        # building
        line = NoteContentLine.of(idx = line_idx, elements = one_line_stack)

        lines.append(line)
        line_idx += 1
        one_line_stack = []
    return lines


def build_paragraph_list(content_lines: List[NoteContentLine]) -> Sequence[NoteContentParagraph]:

    # build paragraph
    paragraphs: List[NoteContentParagraph] = []

    paragraph_stack = []
    previous_line = None
    for idx, line in enumerate(content_lines):
        paragraph_stack.append(line)

        if (
            not (previous_line is not None and not line.is_same_paragraph(previous_line))
            and not line.is_paragraph_breaker()
            and idx != len(content_lines) - 1
        ):
            previous_line = line
        else:
            attribute: ParagraphStyle | None = None if len(paragraph_stack) == 0 else paragraph_stack[0].attribute
            paragraph = NoteContentParagraph(attribute = attribute, lines = paragraph_stack)
            paragraphs.append(paragraph)
            paragraph_stack = []
            previous_line = None

    # for paragraph in paragraphs:
    #     logger.debug(f"{paragraph.__repr__()}")

    return paragraphs


class AppleNotesTableConstructor:
    """
    Thanks to the source code from [AppleNotesEmbeddedTable.rb](https://github.com/threeplanetssoftware/apple_cloud_notes_parser/blob/master/lib/AppleNotesEmbeddedTable.rb)
    This class was generated by OpenAI's GPT-4
    """

    LEFT_TO_RIGHT_DIRECTION = "CRTableColumnDirectionLeftToRight"
    RIGHT_TO_LEFT_DIRECTION = "CRTableColumnDirectionRightToLeft"

    TABLE_ROOT_KRY = "com.apple.notes.ICTable"
    TABLE_DIRECTION_KEY = "crTableColumnDirection"

    TABLE_ROW_KEY = "crRows"
    TABLE_COLUMN_KEY = "crColumns"
    TABLE_CELL_KEY = "cellColumns"

    reconstructed_table: List[NoteAttachmentTableCell] = []

    def __init__(self, mergable_data_proto: MergableDataProto):
        self.key_items: List[str] = []
        self.type_items: List[str] = []
        self.table_objects: List[MergeableDataObjectEntry] = []
        self.uuid_items: List[bytes] = []
        self.total_columns = 0
        self.row_indices: Dict[str, int] = {}
        self.column_indices: Dict[int, int] = {}
        self.table_direction = self.LEFT_TO_RIGHT_DIRECTION

        self._rebuild_table(mergable_data_proto)

    def __str__(self):
        string_to_add = " with cells: "
        for row in self.reconstructed_table:
            string_to_add += "\n"
            for column in row:
                string_to_add += f"\t{column}"
        return super().__str__() + string_to_add

    @classmethod
    def get_target_uuid_from_object_entry(cls, object_entry):
        return object_entry.custom_map.map_entry[0].value.unsigned_integer_value

    def parse_rows(self, object_entry):

        rows = object_entry.ordered_set.ordering

        row_indices = {self.uuid_items.index(attachment.uuid): idx for idx, attachment in enumerate(rows.array.attachment)}

        for element in rows.contents.element:
            key_object = self.get_target_uuid_from_object_entry(self.table_objects[element.key.object_index])
            value_object = self.get_target_uuid_from_object_entry(self.table_objects[element.value.object_index])
            if key_object not in row_indices:
                continue
            self.row_indices[value_object] = row_indices[key_object]

    def parse_columns(self, object_entry):

        columns = object_entry.ordered_set.ordering

        column_indices = {self.uuid_items.index(attachment.uuid): idx for idx, attachment in enumerate(columns.array.attachment)}

        for element in columns.contents.element:
            key_object = self.get_target_uuid_from_object_entry(self.table_objects[element.key.object_index])
            value_object = self.get_target_uuid_from_object_entry(self.table_objects[element.value.object_index])
            if key_object not in column_indices:
                continue
            self.column_indices[value_object] = column_indices[key_object]

    def get_cell_for_column_row(self, current_column: int, row: DictionaryElement) -> None | NoteAttachmentTableCell:
        current_row = self.get_target_uuid_from_object_entry(self.table_objects[row.key.object_index])

        target_cell = self.table_objects[row.value.object_index]

        r_idx = self.row_indices[current_row]
        c_idx = self.column_indices[current_column]

        if r_idx is None or c_idx is None:
            return None
        return NoteAttachmentTableCell(column = r_idx, row = c_idx, text = target_cell.note.note_text)

    def get_cell_for_column(self, column) -> List[NoteAttachmentTableCell]:
        current_column = self.get_target_uuid_from_object_entry(self.table_objects[column.key.object_index])
        target_dictionary_object = self.table_objects[column.value.object_index]

        cell_list = map(
            lambda row: self.get_cell_for_column_row(current_column, row),
            target_dictionary_object.dictionary.element
        )
        return [cell for cell in cell_list if cell is not None]

    def parse_table(self, custom_map: MergeableDataObjectMap):
        if not custom_map:
            return

        if self.type_items[custom_map.type] != self.TABLE_ROOT_KRY:
            return

        for map_entry in custom_map.map_entry:
            if self.key_items[map_entry.key] == self.TABLE_ROW_KEY:
                self.parse_rows(self.table_objects[map_entry.value.object_index])
            elif self.key_items[map_entry.key] == self.TABLE_COLUMN_KEY:
                self.parse_columns(self.table_objects[map_entry.value.object_index])

        cell_columns_to_parse = None
        for map_entry in custom_map.map_entry:
            if self.key_items[map_entry.key] == self.TABLE_CELL_KEY:
                cell_columns_to_parse = self.table_objects[map_entry.value.object_index]

        if len(self.row_indices) <= 0 or len(self.column_indices) <= 0 or not cell_columns_to_parse:
            return

        cell_element = cell_columns_to_parse.dictionary.element
        self.reconstructed_table = list(itertools.chain.from_iterable([self.get_cell_for_column(column) for column in cell_element]))

    def _rebuild_table(self, mergable_data_proto: MergableDataProto):

        object_data = mergable_data_proto.mergable_data_object.mergeable_data_object_data

        self.key_items = [key_item for key_item in object_data.mergeable_data_object_key_item]
        self.type_items = [type_item for type_item in object_data.mergeable_data_object_type_item]
        self.uuid_items = [uuid_item for uuid_item in object_data.mergeable_data_object_uuid_item]
        self.table_objects = [object_entry for object_entry in object_data.mergeable_data_object_entry]

        for object_entry in object_data.mergeable_data_object_entry:
            if not object_entry.custom_map or len(object_entry.custom_map.map_entry) == 0:
                continue

            key: int = object_entry.custom_map.map_entry[0].key
            value: str = object_entry.custom_map.map_entry[0].value.string_value

            if self.TABLE_DIRECTION_KEY == self.key_items[key - 1]:
                self.table_direction = value
                break

        for object_entry in object_data.mergeable_data_object_entry:
            if not object_entry.custom_map:
                continue

            if self.TABLE_ROOT_KRY == self.type_items[object_entry.custom_map.type]:
                # fount the table root.
                self.parse_table(object_entry.custom_map)

        # TODO: sort self.reconstructed_table by direction