from django.db import models
from django.utils.translation import gettext_lazy as _
from pgvector.django import VectorExtension, VectorField
from pgvector.django import HnswIndex


class Memory(models.Model):

    class MemoryType(models.TextChoices):
        NOTE = "NOTE", _("NOTE")
        REMINDER = "REMINDER", _("REMINDER")
        PIC = "PIC", _("PIC")

    memory_type = models.CharField(choices = MemoryType.choices,)
    data = models.JSONField(null = True)

    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "memories"


class MemorySyncLog(models.Model):
    biz_id = models.CharField(max_length = 100)
    biz_modified_at = models.DateTimeField(auto_now = True)

    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "memories_sync_log"
        indexes = [
            models.Index(fields = ['biz_modified_at'], name = "idx_biz_modified_at")
        ]
        constraints = [
            models.UniqueConstraint(fields = ['biz_id'], name = 'uk_biz_id')
        ]
        ordering = ["-biz_modified_at"]


class Neuron(models.Model):
    content = models.TextField(null = False)
    embedding = VectorField(dimensions = 1536)

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