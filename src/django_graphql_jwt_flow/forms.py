from datetime import timedelta, datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from . import models
from .apps import app_settings


def get_default_expires_at():
    return timezone.now() + timedelta(days=app_settings.REFRESH_DAYS)


class CreateTokenForm(forms.ModelForm):
    expires_at = forms.DateTimeField(initial=get_default_expires_at, required=True)

    def clean_expires_at(self):
        value: datetime = self.cleaned_data["expires_at"]
        if value < timezone.now():
            raise ValidationError({"expires_at": "Token expires before issue date"})

        return value.astimezone(timezone.utc)

    def save(self, commit=True):
        user 