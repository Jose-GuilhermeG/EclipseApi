#imports
from django.db import models
from core.models import BaseModel
from core.constants import MEDIUM_CHAR_SIZE , LARGE_CHAR_SIZE 
from django.utils.translation import gettext_lazy as _

USER = 'users.User'

# Create your models here.
class Shop(
    BaseModel
):
    name = models.CharField(
        verbose_name=_("Nome da loja"),
        max_length=MEDIUM_CHAR_SIZE,
        unique=True,
        null=False,
        blank=False,
    )
    
    slug = models.SlugField(
        verbose_name=_("Slug da loja"),
        unique=True,
        null=False,
        blank=False
    )
    
    owner = models.OneToOneField(
        verbose_name=_("Proprietário da loja"),
        to=USER,
        related_name='shop',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    
    description = models.TextField(
        verbose_name=_("Descrição da loja"),
        null=True,
        blank=True
    )
    
    contact_phone = models.CharField(
        verbose_name=_("Telefone de contato da loja"),
        max_length=20,
        null=True,
        blank=True
    )
    
    contact_email = models.EmailField(
        verbose_name=_("Email de contato da loja"),
        max_length=LARGE_CHAR_SIZE,
        null=True,
        blank=True
    )
    
    views = models.IntegerField(
        verbose_name=_("Visualizações da loja"),
        default=0,
        null=True,
        blank=True
    )
    
    banner = models.ImageField(
        verbose_name=_("Banner da loja"),
        upload_to="shop/banner/%Y/%m/",
        null=True,
        blank=True
    )
    photo = models.ImageField(
        verbose_name=_("Foto de perfil da loja"),
        upload_to="shop/photo/%Y/%m/",
        null=True,
        blank=True
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("Loja")
        verbose_name_plural = _("Lojas")