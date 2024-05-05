# from ..web.component import Component
from typing import List

from loci.domain.entity.memory import Memory
from loci.infra.domain.impl.memory import MemoryService

import logging

logger = logging.getLogger(__name__)


class MemoryBizService:

    memory_service = MemoryService()

    def __init__(self):
        logger.info("MemoryBizService init")

    def list_all(self) -> List[Memory]:
        memories = self.memory_service.list_all()
        return memories


service = MemoryBizService()
