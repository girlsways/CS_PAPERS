from django.db import IntegrityError
from django.test import TestCase, SimpleTestCase, override_settings
from jwcrypto.common import json_decode
from jwcrypto.jwk import JWK
from jwcrypto.jwt import JWT

from demo.app.factories import UserFactory
from django_graphql_jwt_flow.models import JwtRefreshTokenManager, Jw