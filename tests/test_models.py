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

    def test_manager_get_or_create(self):
        user = self.create_user()
        user2 = self.create_user()
        expected = JwtRefreshToken.objects.create(user)
        actual, created = JwtRefreshToken.objects.get_or_create(user)
        self.assertEqual(expected.token, actual.token)
        self.assertFalse(created)
        __, created = JwtRefreshToken.objects.get_or_create(user2)
        self.assertTrue(created)

    @override_settings(
        JWT_FLOW={
            "KEY": {"k": "x-A5aHFjJohn3-wuBsv12Q", "kty": "oct"},
            "REFRESH_DAYS": 7,
            "SIGNATURE_ALG": "HS384",
            "TIME_WITH_MICROSECONDS": True,
        }
    )
    def test_manager_refresh_token(self):
        user = self.create_user()
        token = JwtRefreshToken.objects.create(user=user)
        previous_token = token.token
        refreshed = JwtRefreshToken.objects.refresh_token(user)
        self.assertNotEqual(previous_token, refreshed.token)

    def test_manager_disallowed_methods(self):
        first = self.create_user()
        second = self.create_user()
        first_token = JwtRefreshToken.objects.create(user=first)
        second_token = JwtRefreshToken.objects.create(user=second)
        first_token.token = JwtRefreshToken.objects.generate_token(first.pk)
        second_token.token = JwtRefreshToken.objects.generate_token(second.pk)
        with self.assertRaisesMessage(
            TypeError, "Method disallowed. Please use refresh_token()."
        ):
            JwtRefreshToken.objects.update(user=first)
        with self.assertRaisesMessage(
            TypeError, "Method disallowed. Please use refresh_token()."
        ):
            JwtRefreshToken.objects.update_or_create(
                user=second, token=first_token.token
            )

    def test_is_valid_correct(self):
        from django_graphql_jwt_flow.apps import app_settings
        from datetime import datetime, timedelta

        user = self.create_user()
        key = app_settings.get_key()
        now = datetime.utcnow()
        expiration = now + timedelta(seconds=300)
        tk = JWT(
            header={"alg": app_settings.SIGNATURE_ALG},
            claims={"uid": str(user.pk)},
            default_claims={"iat": now.timestamp(), "exp": expiration.timestamp()},
        )
        self.assertIsNotNone(tk)
        tk.make_signed_token(key)
        token = JwtRefreshToken(user=user, token=tk.serialize())
        self.assertTrue(token.is_valid())

    def test_is_valid_signature_incorrect(self):
        user = self.create_user()
        token = JwtRefreshToken.objects.create(user=user)
        token.token = token.token[:-4]
        self.assertFalse(token.is_valid())

    def test_is_valid_object_incorrect(self):
        user = self.create_user()
        token = JwtRefreshToken.objects.create(user=user)
        token.token = token.token[1:]
        self.assertFalse(token.is_valid())

    @override_settings(
        JWT_FLOW={
            "KEY": {"kty": "oct", "k": "J5CnFlrYuU1dITmW8FkD