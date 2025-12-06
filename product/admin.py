from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Product , Category , Evaluation , Doubt

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['name' , 'created_at']
    readonly_fields = ['created_at' , 'created_by' , 'updated_by' , 'updated_at']
    prepopulated_fields = {'slug' : ['name' ]}
    search_fields = ['name']
    search_text_help = _('Buscar por nome')
    list_per_page = 10
    
@admin.register(Category)
class Categoryadmin(admin.ModelAdmin):
    model = Category
    search_fields = ['name']
    search_text_help = _('Buscar por nome')
    readonly_fields = ['created_at' , 'created_by' , 'updated_by' , 'updated_at']
    
@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    ...
    
@admin.register(Doubt)
class DoubtAdmin(admin.ModelAdmin):
    ...
