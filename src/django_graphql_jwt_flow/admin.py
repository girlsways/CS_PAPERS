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

    TokenQuerySet = t.Union[t.Sequence[models.JwtRefreshToken], _TokenQuery