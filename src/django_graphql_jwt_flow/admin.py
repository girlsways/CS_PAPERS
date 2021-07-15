from __future__ import annotations

import typing as t
from datetime import datetime

from django.contrib import admin, messages
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _, ngettext
from jwcrypto.common import json_decode

from django_graphql_jwt_flow.apps import app_settings
from . import models, forms

if t.TYPE_CHECKING:
    from django.db.models.query import QuerySet
    from django.http import HttpRequest
    from django.contrib.auth.base_user import AbstractBaseUser

    class _TokenQuerySet(QuerySet):
        def iterator(
            self, chunk_size: int = 2000
        ) -> t.Iterator[models.JwtRefreshToken]:
            ...

    TokenQuerySet = t.Union[t.Sequence[models.JwtRefreshToken], _TokenQuerySet]

    class AuthenticatedRequest(HttpRequest):
        user: AbstractBaseUser = ...


@admin.register(models.JwtRefreshToken)
class JwtRefreshTokenAdmin(admin.ModelAdmin):
    search_fields = ["user__email", "user__first_name", "user__last_name"]
    list_display = ["user_email", "token_payload", "is_expired"]
    add_form = forms.CreateTokenForm
    actions = ["refresh_token_action"]

    def user_email(self, obj: models.JwtRefreshToken) -> str:
        return obj.user.email

    user_email.short_description = _("Email")

    def token_payload(self, obj: models.JwtRefreshToken) -> str:
        header, payload, sig = obj.token.split(".")
        return urlsafe_base64_decode(payload).decode()

    token_payload.short_description = _("Payload")

    def is_expired(self, obj: models.JwtRefreshToken) -> bool:
        now = datetime.utcnow().timestamp()
        token_payload = json_decode(self.token_payload(obj))
        return now > token_payload["exp"]

    is_expired.boolean = True
    is_expired.short_description = _("Expired?")

    def get_form(self, request, obj=None, **kwargs):
     