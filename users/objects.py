from django.db import models


class PurchasedManager(models.Manager):
    def create(self, **kwargs):
        quantity = kwargs.get("quantity")
        product_price = kwargs.get("product").price
        kwargs["total"] = quantity * product_price
        return super().create(**kwargs)
