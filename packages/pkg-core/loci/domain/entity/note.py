import pymongo
from pymongo import IndexModel

from .memory import Memory, MemoryType
from .. import Note


class MemoryNote(Memory[Note]):
    memory_type: MemoryType = MemoryType.APPLE_NOTES
