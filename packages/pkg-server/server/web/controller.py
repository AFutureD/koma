from abc import ABC, abstractmethod

from .application import Application


class Controller(ABC):

    @abstractmethod
    def __init__(self, app: Application):
        pass
