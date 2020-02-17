from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


def _get_email_field():
    return User.EMAIL_FIELD if User.EMAIL_FIELD != User.USERNAME_FIELD else None


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": (User.USERNAME_FIELD, "password")}),
        (
            _("Personal info"),
     