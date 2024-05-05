from contextlib import asynccontextmanager

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from .web.application import Application
from .interface import memory_router
from loci.domain import Memory
from .globals import CONNECTION_STRING



@asynccontextmanager
async def configure(app: Application):
    mongodb_client = AsyncIOMotorClient(CONNECTION_STRING)

    await init_beanie(database = mongodb_client.get_database('qa'), document_models = [Memory])

    app.include_router(memory_router, prefix = "/memories")

    yield



