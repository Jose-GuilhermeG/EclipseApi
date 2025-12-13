from django.contrib import admin
from core.admin import BaseModelAdmin
from workplace.models import Shop


# Register your models here.
@admin.register(Shop)
class ShopAdmin(BaseModelAdmin): ...
