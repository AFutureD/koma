from __future__ import annotations
from ninja import Schema
from typing import List, TypeVar, Generic

from pydantic import BaseModel

T = TypeVar("T")

class Result(Generic[T], Schema):
    data: T | None = None
    message: str | None = None
    code: int
    success: bool

    @staticmethod
    def succ(data: T) -> Result[T]:
        return Result(data=data, code=200, success=True)

    @staticmethod
    def error(message: str, code: int) -> Result[T]:
        return Result(message=message, code=code, success=False)