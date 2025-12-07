from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

USER = settings.AUTH_USER_MODEL

# Create your models here.
class IsActive(models.Model):
    is_active = models.BooleanField(
        _("Está Ativo?"),
        default=True
    )
    
    class Meta:
        abstract = True
        
class TimeMonitored(models.Model):
    created_at = models.DateTimeField(
        _("Criado em"),
        auto_now_add=True,
    )
    
    updated_at =  models.DateTimeField(
        _("Atualizado em"),
        auto_now=True,
    )
    
    class Meta:
        abstract = True
        
class UserMonitored(models.Model):
    created_by = models.ForeignKey(
        verbose_name=_("Criado por"),
        to=USER,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created_by",
        null=True
    )
    
    updated_by = models.ForeignKey(
        verbose_name=_("atualizado por"),
        to=USER,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated_by",
        null=True
    )
    
    class Meta:
        abstract = True
        
class BaseModel(
    UserMonitored,
    TimeMonitored,
    IsActive,
):
      
    class Meta:
        abstract = True