from django.db import models
from django.utils.translation import gettext_lazy as _


class MemoryType(models.TextChoices):
    NOTE = "NOTE", _("NOTE")
    REMINDER = "REMINDER", _("REMINDER")
    PIC = "PIC", _("PIC")


class IndexState(models.TextChoices):
    NOT_STARTED = "NOT_STARTED", _("not started")
    PROCESSING = "PROCESSING", _("processing")
    INDEXED = "INDEXED", _("indexed")


class EmbedModel(models.TextChoices):
    OPENAI_TEXT_EMBEDDING_3_LARGE = "OPENAI_TEXT_EMBEDDING_3_LARGE", _("openai text-embedding-3-large")
    OPENAI_TEXT_EMBEDDING_3_SMALL = "OPENAI_TEXT_EMBEDDING_3_SMALL", _("openai text-embedding-3-small")
