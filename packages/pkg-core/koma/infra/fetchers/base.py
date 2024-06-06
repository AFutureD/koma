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
        pass

    def release(self):
        self.shutdown()

    def start_fetch(self) -> List[Note]:
        raise NotImplementedError

    def start_render(self):
        for note in self.notes:
            self.renderer.pre_render(note)
            note.render(self.renderer)
            self.renderer.post_render(note)

    def finish(self):
        pass

    def start(self):
        self.notes = self.start_fetch()

        self.start_render()

        self.finish()
