import abc
from typing import List

from ..entity.memory import Memory


class MemoryProtocol(abc.ABC):

    @abc.abstractmethod
    def list_all(self) -> List[Memory]:
        pass
