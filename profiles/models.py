from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

import re

def validate_company_name(value):
    if not re.match(r'^[A-Za-z0-9\s-]{2,110}$', value):
        raise ValidationError("The company name is invalid!")

def validate_secret_key(value):
    if len(value) != 4 or len(set(value)) != 4 or not value.isdigit():
        raise ValidationError("Your secret key must have 4 unique digits!")

def validate_phone_number(value):
    if not value.isdigit():
        raise ValidationError("Phone number must contain only digits.")

class Organizer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Organizer')
    company_name = models.CharField(
        max_length=110,
        unique=True,
        validators=[validate_company_name],
        help_text="*Allowed names contain letters, digits, spaces, and hyphens.",
    )
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[validate_phone_number],
        error_messages={
            'unique': "That phone number is already in use!"
        }
    )
    secret_key = models.CharField(
        max_length=4,
        validators=[validate_secret_key],
        help_text="*Pick a combination of 4 unique digits.",
    )
    website = models.URLField(
        blank=True,
        null=True,
    )

    @property
    def upcoming_events(self):
        return self.events.filter(start_time__gt=timezone.now()).order_by('start_time')

    def __str__(self):
        return self.company_name