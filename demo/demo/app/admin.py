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
            None,
            {
                "classes": ("wide",),
                "fields": (User.USERNAME_FIELD, "password1", "password2"),
            },
        ),
    )
    ordering = (User.USERNAME_FIELD,)
    list_display = ("first_name", "last_name", "is_staff")

    def get_list_display(self, request):
        if User.USERNAME_FIELD == getattr(User, "EMAIL_FIELD", None):
            return (User.USERNAME_FIELD,) + self.list_display
        else:
            return (User.USERNAME_FIELD, User.EMAIL_FIELD) + self.list_display

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            if request.user.pk != getattr(obj, "pk", None):
                return False

        return True
