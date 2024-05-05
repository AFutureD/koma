from __future__ import annotations
from abc import ABC, abstractmethod

from pydantic import BaseModel


class BaseRenderer(ABC):

    @abstractmethod
    def render(self, renderable: RenderAble) -> str:
        pass


class RenderAble(BaseModel):
    rendered: bool = False

    represent: str | None = None

    def render(self, renderer: BaseRenderer):
        if self.rendered:
            return self.represent

        for prop in self.__dict__.values():
            if isinstance(prop, RenderAble):
                prop.render(renderer)
            elif isinstance(prop, list):
                for item in prop:
                    if isinstance(item, RenderAble):
                        item.render(renderer)
            elif isinstance(prop, dict):
                for item in prop.values():
                    if isinstance(item, RenderAble):
                        item.render(renderer)

        self.rendered = True
        if isinstance(self, RenderAble):
            represent = renderer.render(self)
            self.represent = represent
        else:
            raise RuntimeError(f"Unknown type {type(self)}")