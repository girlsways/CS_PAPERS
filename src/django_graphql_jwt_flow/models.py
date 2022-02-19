from __future__ import annotations

import typing as t
from datetime import datetime, timedelta
from json.decoder import JSONDecodeError

from django.contrib.auth import get_user_model
from django.db import models, IntegrityError
from django.utils.translation import gettext_lazy as _
from jwcrypto import jwt
from jwcrypto.common import json_decode
from jwcrypto.jws import InvalidJWSSignature, InvalidJWSObject

__all__ = ("JwtRefreshToken", "JwtRefreshTokenManager")

if t.TYPE_CHECKING:  # pragma: no cover
    from django.contrib.auth.base_user import AbstractBaseUser

    CustomUser = t.TypeVar("CustomUser", bound=AbstractBaseUser)
    JSONScalars = t.Union[int, str, float, bytes, bytearray, bool, None]

User: t.Type[CustomUser] = get_user_model()


class JwtRefreshTokenManager(models.Manager):
    def create(self, user: User):
        if hasattr(user, "jwt_refresh_token"):
            raise IntegrityError(f"User {user.get_username()} already has a token")
        return super().create(
            user=user, token=self.generate_token(str(user.pk)).serialize()
        )

    def get_or_create(self, user: User) -> t.Tuple[J