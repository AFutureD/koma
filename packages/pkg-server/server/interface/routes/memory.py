# from .router import router
from typing import List

from fastapi import APIRouter

from loci.domain.entity import Memory
from ...service import memory_biz_service

router = APIRouter()


@router.get("/list.json")
def read_root() -> List[Memory]:
    memories = memory_biz_service.list_all()
    return memories
