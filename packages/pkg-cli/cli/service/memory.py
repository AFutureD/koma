from typing import List

from loci.domain import Memory
from loci.infra.domain.impl import MemoryService


class MemoryBizService:

    memory_service = MemoryService()

    async def list_all(self) -> List[Memory]:
        memories = await self.memory_service.list_all()
        return memories

    async def sync_notes(self, inc):
        if inc:
            await self.memory_service.sync_notes(inc)
        else:
            pass