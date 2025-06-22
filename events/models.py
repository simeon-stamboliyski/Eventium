from django.db import models
from django.utils import timezone
from profiles.models import Organizer

class Event(models.Model):
    slogan = models.CharField(
        max_length=120,
        blank=False,
        null=False,
    )
    location = models.CharField(
        max_length=120,
        blank=False,
        null=False,
    )
    start_time = models.DateTimeField(
        default=timezone.now,
    )
    available_tickets = models.PositiveIntegerField(
        default=0,
    )
    key_features = models.TextField(
        blank=True,
        null=True,
    )
    banner_url = models.URLField(
        blank=True,
        null=True,
    )
    organizer = models.ForeignKey(
        Organizer,
        on_delete=models.CASCADE,
        related_name='events',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.slogan} at {self.location}"