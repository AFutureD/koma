from __future__ import annotations
from abc import ABC, abstractmethod

from pydantic import BaseModel


class BaseRenderer(ABC):

    @abstractmethod
    def render(self, renderable: RenderAble) -> str:
        ...


class RenderAble(BaseModel):
    rendered: bool = False

    represent: str | None = None

    def render(self, renderer: BaseRenderer):
        if self.rendered:
            return

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
        assert isinstance(self, RenderAble), f"{self.__class__.__qualname__} must be RenderAble"

        represent = renderer.render(self)
        self.represent = represent