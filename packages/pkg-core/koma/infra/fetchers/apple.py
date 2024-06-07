import itertools
import logging
import sqlite3
import zlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, MutableSequence, Sequence, override


from ...domain import (
    AttributeText,
    Note,
    NoteAttachment,
    NoteContent,
    NoteContentLine
)
from ...infra.helper import AppleNotesTableConstructor, build_note_attribute, build_paragraph_list, build_content_lines
from ...infra.renderers import Renderer
from ...protobuf import (
    AttributeRun,
    MergableDataProto,
    NoteStoreProto,
)
from .base import BaseFetcher

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


ALL_NOTES_QUERY = """
SELECT
    note.z_pk as z_pk,
    note.zidentifier AS uuid,
    'x-coredata://' || zmd.z_uuid || '/ICNote/p' || note.z_pk AS url_scheme,
    note.ztitle1 AS title,
    folder.ztitle2 AS folder,
    datetime(note.zmodificationdate1 + 978307200, 'unixepoch') AS modified_at,
    note.ZWIDGETSNIPPET AS preview,
    COALESCE(note.ZACCOUNT, note.ZACCOUNT1, note.ZACCOUNT2, note.ZACCOUNT3, note.ZACCOUNT4, 
             note.ZACCOUNT5, note.ZACCOUNT6, note.ZACCOUNT7, note.ZACCOUNT8) AS account,
    (note.zispasswordprotected = 1) as locked,
    (note.zispinned = 1) as pinned,
    bolb.ZDATA as content
FROM 
    ziccloudsyncingobject AS note
INNER JOIN ziccloudsyncingobject AS folder 
    ON note.zfolder = folder.z_pk
LEFT JOIN z_metadata AS zmd ON 1=1
LEFT JOIN ZICNOTEDATA AS bolb ON note.ZNOTEDATA = bolb.Z_PK
WHERE
    note.ztitle1 IS NOT NULL AND
    note.zmodificationdate1 IS NOT NULL AND
    note.z_pk IS NOT NULL AND
    note.zmarkedfordeletion != 1 AND
    folder.zmarkedfordeletion != 1 AND
    note.zispasswordprotected = 0
ORDER BY
    note.zmodificationdate1 DESC
"""

ALL_ATTACHMENTS_QUERY = """
SELECT
    attachment.Z_PK as z_pk,
    attachment.ZIDENTIFIER as attachment_identifier,
    COALESCE(attachment.ZTYPEUTI, attachment.ZTYPEUTI1) as attachment_uti,
    COALESCE(attachment.ZNOTE, attachment.ZNOTE1) as note_pk,
    COALESCE(attachment.ZACCOUNT, attachment.ZACCOUNT1, attachment.ZACCOUNT2, attachment.ZACCOUNT3, attachment.ZACCOUNT4,
            attachment.ZACCOUNT5, attachment.ZACCOUNT6, attachment.ZACCOUNT7, attachment.ZACCOUNT8,
             blob.ZACCOUNT, blob.ZACCOUNT1, blob.ZACCOUNT2, blob.ZACCOUNT3, blob.ZACCOUNT4, blob.ZACCOUNT5,
             blob.ZACCOUNT6, blob.ZACCOUNT7, blob.ZACCOUNT8) AS account,
    CASE
        -- url
        WHEN attachment.ZTYPEUTI = 'public.url' THEN attachment.ZTITLE
        -- tag
        WHEN attachment.ZTYPEUTI1 = 'com.apple.notes.inlinetextattachment.hashtag' THEN attachment.ZALTTEXT
        -- table
        WHEN attachment.ZTYPEUTI = 'com.apple.notes.table' THEN attachment.ZSUMMARY
        -- draw
        WHEN attachment.ZTYPEUTI = 'com.apple.paper' THEN attachment.ZSUMMARY
        WHEN attachment.ZTYPEUTI = 'com.apple.drawing.2' THEN attachment.ZSUMMARY
        WHEN attachment.ZTYPEUTI = 'com.apple.drawing' THEN attachment.ZSUMMARY
        -- gallery
        WHEN attachment.ZTYPEUTI = 'com.apple.notes.gallery' THEN attachment.ZTITLE
        -- media
        WHEN attachment.ZMEDIA is not null THEN attachment.ZOCRSUMMARY -- ZOCRSUMMARY + ZIMAGECLASSIFICATIONSUMMARY
        ELSE null
    END as attachment_text,
    COALESCE(attachment.ZPARENTATTACHMENT, attachment.ZPARENTATTACHMENT1) as parent_pk,
    -- attachment.ZISPASSWORDPROTECTED as locked
    -- generation used for media and drawing
    COALESCE(attachment.ZFALLBACKIMAGEGENERATION, blob.ZGENERATION, blob.ZGENERATION1) as generation,

    -- url public.url
    attachment.ZURLSTRING as url,
    -- list all tables com.apple.notes.table or com.apple.notes.gallery
    attachment.ZMERGEABLEDATA1 as blob_data,
    -- list all drawing 'com.apple.paper' 'com.apple.drawing.2' 'com.apple.drawing'
    attachment.ZHANDWRITINGSUMMARY as draw_summary,
    -- MEDIA attachment.ZMEDIA as media_pk,
    blob.ZIDENTIFIER as file_uuid,
    blob.ZFILENAME as file_name
from ZICCLOUDSYNCINGOBJECT as attachment
LEFT JOIN ZICCLOUDSYNCINGOBJECT as blob
    on  attachment.ZMEDIA = blob.Z_PK and blob.ZATTACHMENT1 = attachment.Z_PK
WHERE
    (attachment.ZTYPEUTI is not null or attachment.ZTYPEUTI1 is not null)
    and attachment.ZISPASSWORDPROTECTED = 0
    and attachment.ZNEEDSINITIALFETCHFROMCLOUD = 0
"""

ALL_ACCOUNT_QUERY = """
SELECT Z_PK, ZNAME, ZIDENTIFIER FROM ZICCLOUDSYNCINGOBJECT WHERE ZUSERRECORDNAME IS NOT NULL;
"""


class AppleNotesAccount:
    z_pk: int
    name: str
    identifier: str

    def __init__(self, z_pk, name, identifier):
        self.z_pk = z_pk
        self.name = name
        self.identifier = identifier


class AppleNotesFetcher(BaseFetcher):
    GZIP_BLOB_HEADER_OFFSET = 15 + 32
    NOTE_FOLDER_ROOT = Path.home() / "./Library/Group Containers/group.com.apple.notes/"
    NOTE_STORE_PATH = NOTE_FOLDER_ROOT / "NoteStore.sqlite"
    NOTE_MEDIA_ROOT = NOTE_FOLDER_ROOT / "Accounts/"

    connection: sqlite3.Connection

    attachments: List[NoteAttachment] = []
    attachment_map_by_identifier: Dict[str, NoteAttachment] = {}

    accounts: List[AppleNotesAccount] = []
    account_by_pk_map: Dict[int, AppleNotesAccount] = {}

    def __init__(self, renderer: Renderer):
        super().__init__(renderer)
        self.connection = sqlite3.connect(self.NOTE_STORE_PATH.resolve())

    @override
    def shutdown(self):
        if self.connection is not None and self.connection is sqlite3.Connection:
            self.connection.close()

    @override
    def start_fetch(self) -> List[Note]:
        self.list_account_list()
        self.list_all_attachments()
        self.build_attachment_hierarchy()
        return self.list_all_notes()

    @override
    def finish(self):
        for note in self.notes:
            logger.info(f"{note.__repr__()}")


    def list_account_list(self):
        account_rows = []
        cursor = self.connection.cursor()
        try:
            res = cursor.execute(ALL_ACCOUNT_QUERY)
            account_rows = res.fetchall()
        except Exception as e:
            print("ERROR", e)
        finally:
            cursor.close()

        accounts = []
        for z_pk, name, identifier in account_rows:
            account = AppleNotesAccount(z_pk, name, identifier)
            accounts.append(account)

        self.accounts = accounts
        self.account_by_pk_map = {account.z_pk: account for account in accounts}

    def list_all_attachments(self):
        attachment_rows = []
        cursor = self.connection.cursor()
        try:
            res = cursor.execute(ALL_ATTACHMENTS_QUERY)
            attachment_rows = res.fetchall()
        except Exception as e:
            print("ERROR", e)
        finally:
            cursor.close()

        attachments = []
        for (
            z_pk, attachment_identifier, attachment_uti, note_pk, account_pk, attachment_text, parent_pk,
            generation, url, blob_data, draw_summary, file_uuid, file_name
        ) in attachment_rows:
            # build table before create attachment
            table_cell_list = None
            if attachment_uti == "com.apple.notes.table":
                uncompressed_data = zlib.decompress(blob_data, self.GZIP_BLOB_HEADER_OFFSET)

                store = MergableDataProto()
                store.ParseFromString(uncompressed_data)

                table_cell_list = AppleNotesTableConstructor(store).reconstructed_table

            media_root_path = None
            if account_pk is not None:
                account = self.account_by_pk_map.get(account_pk)
                media_root_path = str(self.NOTE_MEDIA_ROOT / f"{account.identifier}")
            else:
                print("ERROR: account not found. attachment pk: ", z_pk)

            attachment = NoteAttachment(
                type_uti = attachment_uti, z_pk = z_pk, identifier = attachment_identifier, note_pk = note_pk,
                text = attachment_text, parent_pk = parent_pk, generation=generation, url=url,
                table_cell_list=table_cell_list, draw_summary=draw_summary,
                media_root_path=media_root_path, file_uuid=file_uuid, file_name=file_name
            )
            attachments.append(attachment)

        self.attachments = attachments
        self.attachment_map_by_identifier = {attachment.identifier: attachment for attachment in attachments}

    # Build attachment hierarchy
    # for now, we only care about `gallery` type
    #  - gallery
    #     └─ image
    #         └─ media <- build this by sql join
    def build_attachment_hierarchy(self):

        grouped_by_parent_attachment_pk = itertools.groupby(self.attachments, key=lambda x: x.parent_pk)
        parent_pk_to_attachments_map = {k: list(v) for k, v in grouped_by_parent_attachment_pk if k is not None}

        for attachment in self.attachments:
            if attachment.type_uti == "com.apple.notes.gallery":
                attachment.append_children(parent_pk_to_attachments_map[attachment.z_pk])

    def list_all_notes(self) -> List[Note]:
        note_rows = []
        cursor = self.connection.cursor()
        try:
            res = cursor.execute(ALL_NOTES_QUERY)
            note_rows = res.fetchall()
        except Exception as e:
            print("ERROR", e)
        finally:
            cursor.close()

        notes = []
        for (
            z_pk, uuid, url_scheme, title, folder, modified_at, preview, account, locked, pinned, gzip_content
        ) in note_rows:

            # if uuid != '43EBA8F2-6FEA-470B-B943-4314448A0C6B':
            #     continue

            utc_modified_at = datetime.strptime(modified_at, "%Y-%m-%d %H:%M:%S")
            local_modified_at = utc_modified_at.replace(tzinfo=timezone.utc).astimezone()

            content = self.build_doc_content(compressed_data=gzip_content)

            note = Note(z_pk = z_pk, uuid = uuid, navigation_link =f'applenotes:note/{uuid}', title = title, folder_name = folder, modified_at = local_modified_at, preview = preview, account_pk = account, locked =locked == 1, pinned =pinned == 1, content = content)
            notes.append(note)

        return notes

    def build_doc_content(self, compressed_data: bytes) -> NoteContent:
        uncompressed_data = zlib.decompress(compressed_data, self.GZIP_BLOB_HEADER_OFFSET)

        store = NoteStoreProto()
        store.ParseFromString(uncompressed_data)

        note_raw = store.document.note
        attribute_text_list = self.build_attribute_text(note_raw.note_text, note_raw.attribute_run)

        doc_content_lines: List[NoteContentLine] = build_content_lines(attribute_text_list)
        doc_paragraph_list = build_paragraph_list(doc_content_lines)

        content = NoteContent(plan_text = note_raw.note_text, attributed_text = attribute_text_list, paragraph_list = doc_paragraph_list)
        return content

    def build_attribute_text(self, plan_text: str, attribute_run_list: Sequence[AttributeRun]) -> Sequence[AttributeText]:
        struct_list: MutableSequence[AttributeText] = []

        # apple note use utf-16
        utf16_text = plan_text.encode("utf-16le")

        cur_idx = 0
        for attribute_run in attribute_run_list:
            length = attribute_run.length * 2  # utf-16 length

            # text and attribute
            text = utf16_text[cur_idx: cur_idx + length].decode("utf-16le")
            attribute = build_note_attribute(attribute_run)
            
            # logger.debug(f"attribute before: ({text_format.MessageToString(attribute_run, as_one_line=True)})")
            # logger.debug(f"attribute after : {attribute.__repr__()}")

            # attachment
            if identifier := attribute.attachment_identifier:
                attribute.attachment = self.attachment_map_by_identifier.get(identifier)

            # notice: we convert apple note length to utf-8 length
            node = AttributeText(start_index = cur_idx, length = len(text), text = text, attribute = attribute)

            cur_idx += length
            struct_list.append(node)

        assert cur_idx == len(utf16_text)
        return struct_list
    
