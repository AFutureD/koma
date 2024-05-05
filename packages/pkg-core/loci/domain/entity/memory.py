from datetime import datetime
from enum import Enum
from typing import Generic, TypeVar, Annotated

import pymongo
from beanie import Document, Indexed
from pymongo import IndexModel

MemoryDataT = TypeVar('MemoryDataT')


class MemorySyncLog(Document):
    biz_id: Annotated[str, Indexed(unique=True)]
    biz_modified_at: datetime

    updated_at: datetime = datetime.now()
    created_at: datetime = datetime.now()

    class Settings:
        name = "memories_sync_log"


class MemoryType(str, Enum):
    """
    https://developer.apple.com/documentation/uniformtypeidentifiers/system-declared_uniform_type_identifiers?language=objc
    """
    APPLE_NOTES = "com.apple.Notes"
    APPLE_REMINDER = "com.apple.reminders"


class Memory(Document, Generic[MemoryDataT]):

    memory_type: MemoryType
    data: MemoryDataT

    updated_at: datetime = datetime.now()
    created_at: datetime = datetime.now()

    class Settings:
        name = "memories"
        indexes = [
            IndexModel(
                [("memory_type", pymongo.ASCENDING)],
                name="key_memory_type",
            ),
            IndexModel(
                [("updated_at", pymongo.DESCENDING)],
                name="key_updated_at",
            ),
        ]
