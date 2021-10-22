from datetime import timedelta, datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from . import models
from .apps import app_settings


def get_default_expires_at():
    return timezone.now() + timedelta(days=app_settings.REFRESH_DAYS)


class CreateTokenForm(forms.ModelForm):
    expires_at = forms.DateTimeField(initi