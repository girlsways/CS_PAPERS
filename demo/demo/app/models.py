
import typing as t

from django.contrib.auth.models import (
    AbstractUser,
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    @classmethod
    def normalize_email(cls, email):
        return email.lower()

    def create_user(self, email: str, password: t.Optional[str] = None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self, email: str, password: t.Optional[str] = None, **extra_fields
    ):
        extra_fields.update(is_superuser=True, is_staff=True)