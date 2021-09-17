
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
    A safe-guard is built in, if one calls a `get_asymmetric_key()`, while the
    configuration is set to symmetric key usage to raise a TypeError. The same
    applies to `get_symmetric_key()`.
    The exception can be suppressed by setting ``raise_exception`` to ``False``.

    """

    def __init__(self, dict_name: str):
        self.dict_name = dict_name
        self._django_settings = None

    @property
    def django_settings(self) -> t.Dict[str, t.Any]:
        from django.conf import settings

        django_settings: t.Dict[str, t.Any] = getattr(settings, self.dict_name, {})
        assert isinstance(django_settings, dict)

        return django_settings

    @property
    def KEY_FORMAT(self) -> str:
        return self.django_settings.get("KEY_FORMAT", "DICT")

    @property
    def KEY(self) -> t.Optional[t.Union[str, bytes, t.Dict[str, str]]]:
        return self.django_settings.get("KEY")

    @property
    def KEY_FILE(self) -> t.Optional[Path]:
        key_file: t.Optional[t.Union[str, Path]] = self.django_settings.get("KEY_FILE")
        if key_file:
            if not isinstance(key_file, Path):
                key_file = Path(key_file)

            key_file = key_file.resolve()
            if not key_file.exists():
                raise FileNotFoundError(f"{key_file}: File does not exist")

        return key_file

    @property
    def REFRESH_DAYS(self) -> int:
        return self.django_settings.get("REFRESH_DAYS", 7)

    @property
    def SIGNATURE_ALG(self) -> str:
        return self.django_settings.get("SIGNATURE_ALG", "HS384")

    @property
    def ALLOWED_SKEW(self) -> int:
        return self.django_settings.get("ALLOWED_SKEW", 90)

    @property
    def TIME_WITH_MICROSECONDS(self) -> bool:
        return self.django_settings.get("TIME_WITH_MICROSECONDS", False)

    @property
    def CHANGE_PERM_SUPERUSER_ONLY(self) -> bool:
        return self.django_settings.get("CHANGE_PERM_SUPERUSER_ONLY", True)

    @property
    def DELETE_PERM_SUPERUSER_ONLY(self) -> bool:
        return self.django_settings.get("DELETE_PERM_SUPERUSER_ONLY", True)

    def get_key(self) -> jwk.JWK:
        """
        Primary method to get the right key.

        :return: The key configured to use by default.
        """
        if self.KEY_FILE: