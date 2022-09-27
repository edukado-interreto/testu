from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group

from .forms import UserCreationForm
from .models import User

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ["email", "username",  "date_joined", "is_active", "is_staff"]
    ordering = ["-id"]
    fieldsets = [
        (None, {"fields": ("email", "data")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        (
            "Advanced",
            {
                "classes": ("collapse",),
                "fields": ["password", "is_active", "is_staff", "is_superuser"],
            },
        ),
    ]

    add_form = UserCreationForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )
