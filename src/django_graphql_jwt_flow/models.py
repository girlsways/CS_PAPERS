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

    CustomUser = t.TypeVar("Cust