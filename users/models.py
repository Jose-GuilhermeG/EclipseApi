from django.db import models
from core.models import BaseModel
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

USER = get_user_model()

# Create your models here.
class ShoppingCar(
    BaseModel
):
    user = models.OneToOneField(
        to=USER,
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
        verbose_name=_("Quantity"),
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