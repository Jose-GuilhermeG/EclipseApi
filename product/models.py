from django.db import models
from core.models import BaseModel
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from core.constants import MEDIUM_CHAR_SIZE , LARGE_CHAR_SIZE
from django.core.validators import MinValueValidator , MaxValueValidator
from django.conf import settings
from django.db.models import Avg
from .objects import ProductManager , CategoryManager
from workplace.models import Shop

USER = settings.AUTH_USER_MODEL

# Create your models here.
class Product(BaseModel):
    name = models.CharField(
        verbose_name=_("Nome do produto"),
        max_length=MEDIUM_CHAR_SIZE,
        unique=False,
        null=False,
        blank=False,
    )
    
    slug = models.SlugField(
        verbose_name=_("Slug do produto"),
        unique=True,
        null=False,
        blank=False
    )
    
    price = models.DecimalField(
        verbose_name=_("Preço do produto"),
        max_digits=6,
        decimal_places=2,
        null=False,
        blank=False,
        validators=[
            MinValueValidator(0)
        ]
    )
    
    description = models.TextField(
        verbose_name=_("Descrição do produto"),
        null=False,
        blank=True
    )
    
    image = models.ImageField(
        verbose_name=_("Imagem do Produto"),
        upload_to="products/images/%Y/%m/",
        blank=True,
        null=True
    )
    
    categorys = models.ManyToManyField(
        verbose_name=_("Categorias do produto"),
        to='product.Category',
        related_name='product',
    )
    
    views = models.IntegerField(
        verbose_name=_("Visualizações do produto"),
        default=0,
        null=True,
        blank=True
    )
    
    shop = models.ForeignKey(
        to=Shop, 
        verbose_name=_("Loja"), 
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True
    )
    
    objects = ProductManager()
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("product:product-detail", kwargs={"slug": self.slug})
    
    def get_rating(self):
        return self.evaluations.aggregate(avg_rating=Avg("rating"))['avg_rating'] or 0
        
    def get_evaluations_number(self):
        return self.evaluations.count()    
    
    class Meta:
        verbose_name = _("Produto")
        verbose_name_plural = _("Produtos")
        ordering = ['-price']
        
class Category(BaseModel):
    name = models.CharField(
        verbose_name=_("Nome da categoria"),
        max_length=MEDIUM_CHAR_SIZE,
        unique=True,
        null=False,
        blank=False
    )
    
    slug = models.SlugField(
        verbose_name=_("Slug da categoria"),
        unique=True,
        null=False,
        blank=False
    )
    
    objects = CategoryManager()
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("Categoria")
        verbose_name_plural = _("Categorias")
        
class Evaluation(BaseModel):
    product = models.ForeignKey(
        verbose_name=_("Produto avaliado"),
        to=Product,
        related_name="evaluations",
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    
    user = models.ForeignKey(
        verbose_name=_("Usuário que avaliou"),
        to=USER,
        related_name="evaluations",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    rating = models.PositiveSmallIntegerField(
        verbose_name=_("Avaliação do produto"),
        null=False,
        blank=False,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )
    
    comment = models.TextField(
        verbose_name=_("Comentário da avaliação"),
        null=True,
        blank=True
    )
    
    def __str__(self):
        return f"{self.product.name} - {self.rating}"
    
    def get_absolute_url(self):
        return reverse("product:evaluations-detail", kwargs={"pk": self.pk , "slug" : self.product.slug })
    
    
    class Meta:
        verbose_name = _("Avaliação")
        verbose_name_plural = _("Avaliações")
        ordering = ['-created_at']
        
class Doubt(BaseModel):
    title = models.CharField(
        verbose_name=_("Titulo da duvida"),
        max_length=LARGE_CHAR_SIZE ,
        null=False,
        blank=False
    )
    
    product = models.ForeignKey(
        verbose_name=_("Produto"),
        to=Product,
        related_name='doubts',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    
    user = models.ForeignKey(
        verbose_name=_("Usuário"),
        to=USER,
        related_name="doubts",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    content = models.TextField(
        verbose_name=_("Conteudo da duvida"),
        blank=False,
        null=False,
    )
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("product:product_doubt_edit", kwargs={"id": self.pk , "slug" : self.product.slug })
    
    class Meta:
        verbose_name = _("Duvida")
        verbose_name_plural = _("Duvidas")