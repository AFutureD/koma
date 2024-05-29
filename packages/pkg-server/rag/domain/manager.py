from typing import List, override

from django.db import models
from django.db.models import QuerySet
from pgvector.django import CosineDistance

from .models import Neuron, Memory

MODEL_MANAGER_ATTRIBUTE = 'objects'


class MemoryManager(models.Manager[Memory]):

    def __init__(self):
        super().__init__()
        self.contribute_to_class(Memory, MODEL_MANAGER_ATTRIBUTE)

    def list_all(self) -> List[Memory]:
        return list(self.all())


class NeuronManager(models.Manager[Neuron]):

    def __init__(self):
        super().__init__()
        self.contribute_to_class(Neuron, MODEL_MANAGER_ATTRIBUTE)

    def list_within_distance_on_embedding(self, embedding: List[float], distance: float) -> List[Neuron]:
        query = self.alias(distance = CosineDistance('embedding', embedding)).filter(distance__lt = distance)
        return list(query)
