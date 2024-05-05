import logging

from .web.application import Application
from .configure import configure


logging.basicConfig(level=logging.DEBUG)

app: Application = Application(lifespan=configure)


@app.get("/health")
async def health_check():
    return {"status": "ok"}