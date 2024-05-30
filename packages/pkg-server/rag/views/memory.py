from typing import List

from ninja import Router


from ..dto.common import Result
from ..dto.memory import MemoryDTO
from ..infra.services import MemoryBizService

router = Router()

memory_biz_service = MemoryBizService()

@router.get('/list.json', response=Result[List[MemoryDTO]])
def list_memories(request) -> Result[List[MemoryDTO]]:
    dto = memory_biz_service.list_all()
    return Result.with_data(dto)


@router.post('/sync.json', response=Result[None])
def sync_memories(request) -> Result[None]:
    memory_biz_service.sync_memories()
    return Result.succ()