from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as modelUserAdmin
from users import models
from django.utils.translation import gettext_lazy as _
from core.admin import BaseModelAdmin


@admin.register(models.User)
class UserAdmin(modelUserAdmin):
    list_display = ["username", "email", "last_login"]
    fieldsets = (
        (
            _("Dados Pessoais"),
            {
                "fields": (
                    "username",
                    "password",
                    "photo",
                    "first_name",
                    "last_name",
                    "email",
                )
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
                "fields": ("username", "usable_password", "password1", "password2"),
            },
        ),
    )


@admin.register(models.ShoppingCar)
class ShoppingCarAdmin(BaseModelAdmin):
    list_display = ("user", "created_at")


@admin.register(models.ShoppingCarItem)
class ShoppingCarItemAdmin(BaseModelAdmin):
    list_display = ["product", "shopping_car"]
    readonly_fields = BaseModelAdmin.readonly_fields + ["total"]


@admin.register(models.Purchased)
class PurchasedAdmin(BaseModelAdmin):
    list_display = ["user", "product", "status"]
    readonly_fields = BaseModelAdmin.readonly_fields + ["total"]
