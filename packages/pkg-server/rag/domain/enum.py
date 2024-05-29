from django.db import models
from django.utils.translation import gettext_lazy as _


class MemoryType(models.TextChoices):
    NOTE = "NOTE", _("NOTE")
    REMINDER = "REMINDER", _("REMINDER")
    PIC = "PIC", _("PIC")