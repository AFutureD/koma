import datetime
import unittest
from unittest import IsolatedAsyncioTestCase

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import Session

import tracemalloc

tracemalloc.start()


class TestEntity(IsolatedAsyncioTestCase):

    async def test_log(self):
        pass
