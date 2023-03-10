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
        user = self.cleaned_data["user"]
        pk = str(user.pk)
        expires_at = self.cleaned_data["expires_at"]
        token = models.JwtRefreshToken.objects.generate_token(pk, expires_at=expires_at)
        self.instance.token = token.serialize()
        return super().save(commit=commit)

    class Meta:
        model = models.JwtRefreshToken
        fields = ("user",)
