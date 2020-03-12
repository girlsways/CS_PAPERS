
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
        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email: str, password: t.Optional[str], **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    EMAIL_FIELD = USERNAME_FIELD
    email = models.EmailField(_("email"), unique=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    objects = UserManager()

    def clean(self):
        super().clean()
        setattr(
            self,
            self.EMAIL_FIELD,
            self.__class__.objects.normalize_email(getattr(self, self.EMAIL_FIELD)),
        )

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(
            subject, message, from_email, [getattr(self, self.EMAIL_FIELD)], **kwargs
        )