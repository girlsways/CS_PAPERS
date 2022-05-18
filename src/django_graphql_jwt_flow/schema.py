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
    from django.contrib.auth.models import AbstractBaseUser

    CustomUserModel = t.TypeVar("CustomUserModel", bound=AbstractBaseUser)

User: t.Type[CustomUserModel] = get_user_model()


class RefreshToken(DjangoObjectType):
    class Meta:
        model = JwtRefreshToken
        fields = ("user", "token")


class Login(graphene.Mutation):
    class Meta:
        arguments = {
            getattr(User, "USERNAME_FIELD", "username"): graphene.Argument(
                graphene.String, required=True
            ),
            "password": graphene.Argument(graphene.String, required=True),
        }

    success = graphene.Boolean()

    @classmethod
    def mutate(
        cls, root: graphene.ObjectType, info: graphene.ResolveInfo, **credentials: str
    ):
        user = authenticate(request=info.context, **credentials)
        if not user:
            raise GraphQLError(ErrorStrings.invali