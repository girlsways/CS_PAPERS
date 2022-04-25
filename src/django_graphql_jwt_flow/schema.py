from __future__ import annotations

import typing as t

import graphene
from django.contrib.auth import authenticate, get_user_model
from graphene_django import DjangoObjectType

from . import apps
from .exceptions import GraphQLError
from .models import JwtRefreshToken
from .wks import ErrorStrings

if t.TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUs