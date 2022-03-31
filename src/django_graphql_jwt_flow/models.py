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

    def get_or_create(self, user: User) -> t.Tuple[JwtRefreshToken, bool]:
        queryset = super().get_queryset()
        try:
            return queryset.get(user=user), False
        except self.model.DoesNotExist:
            return self.create(user), True

    def refresh_token(self, user: User) -> JwtRefreshToken:
        new_token = self.generate_token(uid=str(user.pk))
        return super().update_or_create(
            defaults={"token": new_token.serialize()}, user=user
        )[0]

    def update(self, **kwargs):
        raise TypeError("Method disallowed. Please use refresh_token().")

    def update_or_create(self, defaults=None, **kwargs):
        raise TypeError("Method disallowed. Please use refresh_token().")

    @classmethod
    def generate_token(
        cls,
        uid: str,
        header: t.Dict[str, JSONScalars] = None,
        expires_at: t.Optional[datetime] = None,
        **claims,
    ) -> jwt.JWT:
        from .apps import app_settings

        key = app_settings.get_key()
        claims.update(uid=uid)
        now = datetime.utcnow()
        if not app_settings.TIME_WITH_MICROSECONDS:
            now = now.replace(microsecond=0)
        delta = app_settings.get_expiration_delta()
        expires_at = expires_at or now + delta
        default_claims = {
            "iat": now.timestamp(),
            "exp": expires_at.timestamp(),
        }
        header = header or {}
        header.update(alg=app_settings.SIGNATURE_ALG)
        token = jwt.JWT(header=header, claims=claims, default_claims=default_claims)
        token.make_signed_token(key)
        return token


class JwtRefreshToken(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="jwt_refresh_token",
        verbose_name=_("user"),
    )
    token = models.TextField(verbose_name=_("token"), db_index=True)
    objects = JwtRefreshTokenManager()

    class Meta:
        verbose_name = _("Refresh token (JWT)")
        verbose_name_plural = _("Refresh tokens (JWT)")

    def __str__(self):
        return f"token for user with ID {self.user.pk}"

    def is_valid(self) -> bool:
        """
        Asserts that the user id corrsponds to the pk and that the current time
        is within timerestrictions placed in the claim.

        :return: Whether the token is valid
        """
        from .apps import app_settings

        try:
            token = jwt.JWT(key=app_settings.get_key(), jwt=self.token)
        except (InvalidJWSSignature, InvalidJWSObject):
            return False
        try:
            claims = json_decode(token.claims)
        except (JSONDecodeError, TypeError):  # pragma: no cover
            return False

        now = datetime.utcnow()
     