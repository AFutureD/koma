
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

from loci.domain.models.note import Note
from ..domain.models import Memory, Neuron


class MemoryDTO(BaseModel):
    memory_type: str = Field(title = "The type of the memory.")
    data: Note  # temporary usage
    updated_at: datetime = Field(title = "The last updated time of the memory.")
    created_at: datetime = Field(title = "The created time of the memory.")

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
    content: str = Field(title = "The content of the neuron")
    biz_id: str = Field(title = "The biz id of the original object in memory.")

    @staticmethod
    def from_model(model: Neuron) -> 'NeuronDTO':
        return NeuronDTO(
            content=model.content, biz_id=model.biz_id
        )
    
    @staticmethod
    def from_model_list(models: List[Neuron]) -> List['NeuronDTO']:
        return [NeuronDTO.from_model(model) for model in models]
