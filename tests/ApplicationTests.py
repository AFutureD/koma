import unittest

from packages.server.web.application import Application
from packages.server.configure import configure
from packages.server.web.database import db_lifespan


import uvicorn


class TestApplication(unittest.TestCase):

    def test_entry(self):
        app = Application(lifespan = db_lifespan)
        configure(app)
        uvicorn.run(app)

