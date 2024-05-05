from __future__ import annotations

import logging
from typing import Dict

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

logger = logging.getLogger(__name__)




class Application(FastAPI):
    mongodb_client: None | AsyncIOMotorClient = None
    database: Dict[str, AsyncIOMotorDatabase] = {}
    # components: Dict[str, Component] = {}
    #
    # def register(self, name: str, clz: type[T]) -> T:
    #
    #     if not name or len(name) == 0:
    #         # make sure name is not blank.
    #         name = clz.__name__
    #
    #     component = clz(self)
    #
    #     return self.register_instance_with_name(name, component)
    #
    # def register_instance_with_name(self, name: str, component: type[T]) -> T:
    #     # TODO: add lock
    #     self.components[name] = component
    #     return component
    #
    # def get_component(self, name: str, clz: type[T]) -> T:
    #     # TODO: allow init component if not exists
    #     component = self.components[name]
    #     if not component:
    #         # Create one if empty
    #         component = self.register(name, clz)
    #
    #     assert isinstance(component, clz)
    #
    #     return component
