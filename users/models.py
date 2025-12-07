from django.db import models
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from core.constants import MEDIUM_CHAR_SIZE , LARGE_CHAR_SIZE
from users.enuns import PURCHASEDSTATUS
from users.objects import PurchasedManager

# Create your models here.
class User(
    AbstractUser
):
    username = models.CharField(
        verbose_name=_("Nome do usuario"),
        max_length=MEDIUM_CHAR_SIZE,
        null=False,
        blank=False,
        unique=False
    )
    
    email = models.EmailField(
        verbose_name=_("Email do usuario"),
        max_length=LARGE_CHAR_SIZE,
        blank=False,
        null=False,
        unique=True
    )
    
    photo = models.ImageField(
        verbose_name=_("Foto do usaurio"),
        blank=True,
        null=True,
        upload_to="users/%y/%m/"
    )
    
    def __str__(self):
        return str(self.email)
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = _("Usuario")
        verbose_name_plural = _("Usuarios")


class ShoppingCar(
    BaseModel
):
    user = models.OneToOneField(
        to=User,
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name='shopping_car'
    )
    
    class Meta:
        verbose_name = _("Carrinho de compra")
        verbose_name_plural = _("Carrinho de compras")
        
    def __str__(self):
        return f"Shopping Car of {self.user.username}"
    
class ShoppingCarItem(
    BaseModel
):
    shopping_car = models.ForeignKey(
        to=ShoppingCar,
        verbose_name=_("Carrinho de Compras"),
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        to='product.Product',
        verbose_name=_("Produto"),
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        verbose_name=_("Quantidade"),
        default=1
    )
    
    total = models.DecimalField(
        verbose_name=_("Preço Total"),
        max_digits=10,
        decimal_places=2,
    )
    
    class Meta:
        verbose_name = _("Item do carrinho de compras")
        verbose_name_plural = _("Items dos carrinho de compras")
        unique_together = ('shopping_car' , 'product')
        
    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.shopping_car.user.username}'s car"
    
class Purchased(
    BaseModel
):
    user = models.ForeignKey(
        to=User,
        verbose_name=_("Usuario"),
        related_name="purchased",
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    
    product = models.ForeignKey(
        to="product.Product",
        verbose_name=_("Produto"),
        related_name="purchased",
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    
    quantity = quantity = models.PositiveIntegerField(
        verbose_name=_("Quantidade"),
        default=1
    )
    
    status = models.CharField(
        verbose_name=_("Status do pedido"),
        max_length=2,
        blank=False,
        null=False,
        choices=PURCHASEDSTATUS.choices,
        default=PURCHASEDSTATUS.PENDING,
    )
    
    submit_date = models.DateTimeField(
        verbose_name=_("data de pagamento"),
        blank=True,
        null=True
    )
    
    total = models.DecimalField(
        verbose_name=_("Preço Total"),
        max_digits=10,
        decimal_places=2,
        null=True,
        editable=False
    )
    
    objects = PurchasedManager()
    
    def __str__(self):
        return f"{self.user} - {self.product}"
    
    class Meta:
        verbose_name = _("Pedido")
        verbose_name_plural = _("Pedidos")