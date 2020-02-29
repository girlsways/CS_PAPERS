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
            {
                "fields": [
                    f
                    for f in ("first_name", "last_name", _get_email_field())
                    if f is not None
                ]
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            N