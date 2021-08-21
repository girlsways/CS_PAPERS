
import typing as t
from datetime import timedelta
from pathlib import Path

import jwcrypto.jwk as jwk
from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured


class DjangoGraphqlJwtFlowConfig(AppConfig):
    name = "django_graphql_jwt_flow"
    verbose_name = "Django GraphQL JWT Flow"


class AppSettings:
    """
    Application settings for Django GraphQL JWT Flow

    Gives access to library specific settings and defaults. Also provides a
    number of high-level methods to get the right key.