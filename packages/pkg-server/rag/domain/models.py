from typing import Any

from django.db import models
from pgvector.django import HnswIndex, VectorField
from pydantic import BaseModel

from koma.domain.models.note import Note

from .enum import EmbedModel, IndexState, MemoryType


class AppleNoteField(models.JSONField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        """
        Convert the value from the database to a Python object.
        """
        if value is None:
            return value
        json_value = super().from_db_value(value, expression, connection)
        return Note(**json_value)
    
    def get_prep_value(self, value: Any) -> Any:
        """
        Convert the value to dict to store in the database.
        """
        if value is None:
            return value
        
        if isinstance(value, BaseModel):
            return value.model_dump(mode = 'json')
        else:
            return value

    def to_python(self, value: Any) -> None | Note:
        if value is None:
            return value
        if isinstance(value, Note):
            return value

        if isinstance(value, str):
            import json
            json_value = json.loads(value)
        elif isinstance(value, dict):
            json_value = value
        else:
            return super().to_python(value)
        return Note(**json_value)


class Memory(models.Model):
    memory_id = models.AutoField(primary_key = True)

    memory_type = models.CharField(choices = MemoryType.choices)
    data = AppleNoteField(null=True)

    biz_id = models.CharField(max_length = 100)

    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = "memories"
        constraints = [
            models.UniqueConstraint(fields = ['biz_id'], name = 'uk_biz_id')
        ]


class MemorySyncLog(models.Model):
    log_id = models.AutoField(primary_key = True)

    biz_id = models.CharField(max_length = 100)
    biz_modified_at = models.DateTimeField(auto_now = True)

    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = "memories_sync_log"
        indexes = [
            models.Index(fields = ['biz_modified_at'], name = "idx_biz_modified_at")
        ]
        ordering = ["-biz_modified_at"]


class Position(BaseModel):
    chapter: int | None = None
    section: int | None = None 
    paragraph: int | None = None
    line: int | None = None


class PositionField(models.JSONField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        json_value = super().from_db_value(value, expression, connection)
        return Position(**json_value)
    
    def get_prep_value(self, value: Any) -> Any:
        if value is None:
            return value
        
        if isinstance(value, BaseModel):
            return value.model_dump(mode = 'json', exclude_none = True)
        else:
            return value

    def to_python(self, value: Any) -> None | Position:
        if value is None:
            return value
        if isinstance(value, Position):
            return value

        if isinstance(value, str):
            import json
            json_value = json.loads(value)
        elif isinstance(value, dict):
            json_value = value
        else:
            super().to_python(value)
        return Position(**json_value)


class NeuronIndexLog(models.Model):
    log_id = models.AutoField(primary_key = True)

    memory_id = models.IntegerField()
    state = models.CharField(choices = IndexState.choices, default=IndexState.NOT_STARTED)
    indexed_at = models.DateTimeField(null=True)

    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'neuron_index_logs'
        indexes = [
            models.Index(fields = ['memory_id'], name = 'idx_memory_id')
        ]


class Neuron(models.Model):
    neuron_id = models.AutoField(primary_key = True)

    content = models.TextField(null = False)
    embedding = VectorField(dimensions = 1536)

    memory_id = models.IntegerField()
    position = PositionField(null = True)
    embed_model = models.CharField(choices = EmbedModel.choices)

    class Meta:
        db_table = 'neurons'
        indexes = [
            HnswIndex(
                name = 'idx_hnsw_embedding',
                fields = ['embedding'],
                m = 16,
                ef_construction = 64,
                opclasses = ['vector_cosine_ops']
            )
        ]

    def __str__(self):
        return self.content