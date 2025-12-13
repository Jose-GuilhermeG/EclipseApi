from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Product, Category, Evaluation, Doubt
from core.admin import BaseModelAdmin


# Register your models here.
@admin.register(Product)
class ProductAdmin(BaseModelAdmin):
    model = Product
    list_display = ["name", "created_at"]
    prepopulated_fields = {"slug": ["name"]}
    search_fields = ["name"]
    search_text_help = _("Buscar por nome")


@admin.register(Category)
class Categoryadmin(BaseModelAdmin):
    model = Category
    search_fields = ["name"]
    search_text_help = _("Buscar por nome")


@admin.register(Evaluation)
class EvaluationAdmin(BaseModelAdmin): ...


@admin.register(Doubt)
class DoubtAdmin(BaseModelAdmin): ...
