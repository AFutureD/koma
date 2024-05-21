
from datetime import datetime
from typing import List
from pydantic import BaseModel

from loci.domain.models.note import Note
from ..domain.models import Memory, Neuron


class MemoryDTO(BaseModel):
    memory_type: str
    data: Note  # temporary usage
    updated_at: datetime
    created_at: datetime

    @staticmethod
    def from_model(model: Memory) -> 'MemoryDTO':
        return MemoryDTO(
            memory_type=model.memory_type,
            data=model.data,
            updated_at=model.updated_at,
            created_at=model.created_at,
        )

    @staticmethod
    def from_model_list(models: List[Memory]) -> List['MemoryDTO']:
        return [MemoryDTO.from_model(model) for model in models]


class NeuronDTO(BaseModel):
    content: str

    @staticmethod
    def from_model(model: Neuron) -> 'NeuronDTO':
        return NeuronDTO(
            content=model.content,
        )
    
    @staticmethod
    def from_model_list(models: List[Neuron]) -> List['NeuronDTO']:
        return [NeuronDTO.from_model(model) for model in models]
