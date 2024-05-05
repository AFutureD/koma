import logging

from motor.motor_asyncio import AsyncIOMotorClient

from ..web.application import Application
from ..globals import CONNECTION_STRING

logger = logging.getLogger(__name__)


async def db_lifespan(app: Application):

    mongodb_client = AsyncIOMotorClient(CONNECTION_STRING)

    app.mongodb_client = mongodb_client

    ping_response = await mongodb_client.admin.command("ping")

    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    else:
        logger.info("Connected to database cluster.")

    yield

    mongodb_client.close()


