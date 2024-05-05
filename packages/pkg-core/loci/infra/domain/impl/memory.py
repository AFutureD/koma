import logging
from datetime import datetime
from typing import List

from beanie.odm.operators.find.comparison import In

from ...fetchers import AppleNotesFetcher
from ...renderers import MarkDown
from ....domain import Note
from ....domain.entity.memory import MemoryType, MemorySyncLog
from ....domain.entity.note import MemoryNote
from ....domain.protocol.memory import MemoryProtocol

logger = logging.getLogger(__name__)

class MemoryService(MemoryProtocol):
    async def list_all(self) -> List[MemoryNote]:
        return await MemoryNote.find(MemoryNote.memory_type == MemoryType.APPLE_NOTES).to_list()

    def all_note_list(self) -> List[Note]:
        markdown = MarkDown()
        fetcher = AppleNotesFetcher(markdown)
        fetcher.start()

        return fetcher.notes

    async def sync_notes(self, inc):
        notes = self.all_note_list()

        if len(notes) == 0:
            return

        uuids = list(map(lambda x: x.uuid, notes))
        logs = await self.sync_log(uuids)

        last_modified_map_by_biz_id = {log.biz_id: log.biz_modified_at for log in logs}

        callback_min = datetime(1970, 1, 1).astimezone()
        to_update_notes = list(filter(lambda x: x.modified_at > last_modified_map_by_biz_id.get(x.uuid, callback_min), notes))

        if len(to_update_notes) == 0:
            return

        memories = [
            MemoryNote(
                data=note
            )
            for note in to_update_notes
        ]

        sync_logs = [
            MemorySyncLog(
                biz_id=note.uuid,
                biz_modified_at=note.modified_at
            )
            for note in to_update_notes
        ]

        logger.info(f"Sync {len(memories)} notes")

        await MemoryNote.insert_many(memories)
        await MemorySyncLog.insert_many(sync_logs)

    async def sync_log(self, uuid_list: List[str]) -> List[MemorySyncLog]:
        return await MemorySyncLog.find(
            In(MemorySyncLog.biz_id, uuid_list)
        ).to_list()
