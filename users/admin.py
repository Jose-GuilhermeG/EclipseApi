from django.contrib import admin
from users import models

@admin.register(models.ShoppingCar)
class ShoppingCarAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    
@admin.register(models.ShoppingCarItem)
class ShoppingCarItemAdmin(admin.ModelAdmin):
    list_display = ['product' , 'shopping_car']
    readonly_fields = ['total']