from typing import List

from django.db import models
from pgvector.django import CosineDistance

from .models import Memory, Neuron, MemorySyncLog

MODEL_MANAGER_ATTRIBUTE = 'objects'


class MemoryManager(models.Manager[Memory]):

    def __init__(self):
        super().__init__()
        self.contribute_to_class(Memory, MODEL_MANAGER_ATTRIBUTE)

    def list_all(self) -> List[Memory]:
        return list(self.all())


class MemorySyncLogManager(models.Manager[MemorySyncLog]):
    def __init__(self):
        super().__init__()
        self.contribute_to_class(MemorySyncLog, MODEL_MANAGER_ATTRIBUTE)

    def list_by_biz_ids(self, biz_ids: List[str]) -> List[MemorySyncLog]:
        query = self.filter(biz_id__in = biz_ids)
        return list(query)
    

class NeuronManager(models.Manager[Neuron]):

    def __init__(self):
        super().__init__()
        self.contribute_to_class(Neuron, MODEL_MANAGER_ATTRIBUTE)

    def list_within_distance_on_embedding(self, embedding: List[float], distance: float) -> List[Neuron]:
        query = self.alias(distance = CosineDistance('embedding', embedding)).filter(distance__lt = distance)
        return list(query)
