from django.db.models import signals
from django.dispatch import receiver
from .models import ShoppingCar , ShoppingCarItem
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save , pre_save

USER = get_user_model()


@receiver(post_save , sender=USER)
def create_shopping_car(sender , instance , created , **kwargs):
    if created:
        ShoppingCar.objects.create(
            user = instance
        )
        
@receiver(pre_save , sender=ShoppingCarItem)
def set_shopping_car_total_price(sender , instance  , **kwargs):
    instance.total = instance.product.price * instance.quantity