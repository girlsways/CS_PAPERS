from django.db import IntegrityError
from django.test import TestCase, SimpleTestCase, override_settings
from jwcrypto.common import json_decode
from jwcrypto.jwk import JWK
from jwcrypto.jwt import JWT

from demo.app.factories import UserFactory
from django_graphql_jwt_flow.models import JwtRefreshTokenManager, JwtRefreshToken


class TokenGeneratorTest(SimpleTestCase):
    oct_key = {
        "kty": "oct",
        "k": "-z6e2mZKlX-_9Oa5lw1qaQ",
    }

    @override_settings(
        JWT_FLOW={
            "KEY": oct_key,
            "SIGNATURE_ALG": "HS256",
        }
    )
    def test_oct_hsalg(self):
        token = JwtRefreshTokenManager.generate_token(uid="1")
        serialized = token.serialize()
        key = JWK(**self.oct_key)
        tk = JWT(key=key, jwt=serialized)
        actual = json_decode(tk.claims)
        self.assertEqual(actual["uid"], "1")
        self.assertTrue("exp" in actual)
        self.assertTrue("iat" in actual)


class JwtRefreshTokenTest(TestCase):
    @staticmethod
    def create_user(**overrides):
        return UserFactory(**overrides)

    def test_manager_create(self):
        for i in range(0, 5):
            user = self.create_user()
            self.assertFalse(hasattr(user, "jwt_refresh_token"))
            token = JwtRefreshToken.objects.create(user)
            self.assertTrue(token.is_valid())

    def test_manager_create_user_has_token(self):
        user = self.create_user()
        self.assertFalse(hasattr(user, "jwt_refresh_token"))
        JwtRefreshToken.objects.create(user)
        with self.assertRaisesMessage(
            IntegrityError, f"User {user.get_username()} already has a token"
        ):
            token = JwtRefreshToken.objects.create(user)
