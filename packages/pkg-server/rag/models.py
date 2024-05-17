from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Memory(models.Model):

    class MemoryType(models.TextChoices):
        NOTE = "NOTE", _("NOTE")
        REMINDER = "REMINDER", _("REMINDER")
        PIC = "PIC", _("PIC")

    memory_type = models.CharField(choices = MemoryType.choices,)
    data = models.JSONField(null = True)

    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now = True)
