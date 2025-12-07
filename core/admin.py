from django.contrib import admin

class BaseModelAdmin(admin.ModelAdmin):
    list_per_page = 10
    readonly_fields = ['created_at' , 'created_by' , 'updated_by' , 'updated_at']
    ordering = ['-created_at']

# Register your models here.
