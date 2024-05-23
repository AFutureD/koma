from __future__ import annotations

from types import NoneType

from ninja import Schema
from typing import TypeVar, Generic

from pydantic import BaseModel

T = TypeVar("T")

class Result(Schema, BaseModel, Generic[T]):
    """
    Notice: The inhert order matters.
    """

    code: int
    success: bool
    data: T | None = None
    err: str | None = None

    @staticmethod
    def with_data(data: T) -> Result[T]:
        return Result[T](code=200, success=True, data=data)

    @staticmethod
    def succ() -> Result[None]:
        return Result[None](code = 200, success = True)

    @staticmethod
    def with_err(code: int, err_msg: str) -> Result[None]:
        return Result[None](code=code, success=False, err=err_msg)