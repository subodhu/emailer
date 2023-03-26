from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import SignupForm, UserUpdateForm
from .models import User


@admin.register(User)
class MyUserAdmin(AuthUserAdmin):
    add_form = SignupForm
    form = UserUpdateForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name", "mobile")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )
    list_display = ("email", "name", "mobile", "is_staff", "date_joined")
    search_fields = ("email",)
    ordering = ("-date_joined", "email")
