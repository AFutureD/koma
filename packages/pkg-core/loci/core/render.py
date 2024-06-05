from __future__ import annotations

from abc import ABC, abstractmethod
from pydantic import Field

from .model import Model


class TextRenderer(ABC):
    META_KEY = "TEXT_RENDER_RESULT"

    @abstractmethod
    def render(self, renderable: RenderAble) -> str:
        ...


class RenderAble(Model):

    rendered: bool = Field(default=False, exclude=True)
    rendered_result: str | None = Field(default=None, exclude=True)

    def render(self, renderer: TextRenderer):
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

        render_result = renderer.render(self)
        
        self.metadata[renderer.META_KEY] = render_result
        self.rendered_result = render_result