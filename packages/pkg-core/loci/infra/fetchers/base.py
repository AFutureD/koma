import atexit
from typing import List

from ...infra.renderers import Renderer
from ...domain import Note


class BaseFetcher:
    renderer: Renderer

    notes: List[Note]

    def __init__(self, renderer: Renderer):
        self.renderer = renderer

        atexit.register(self.release)

    def shutdown(self):
        raise NotImplementedError

    def release(self):
        self.shutdown()

    def start_fetch(self) -> List[Note]:
        raise NotImplementedError

    def start_render(self):
        for memory in self.notes:
            self.renderer.start_pipline(memory)

    def finish(self):
        pass

    def start(self):
        self.notes = self.start_fetch()

        self.start_render()

        self.finish()
