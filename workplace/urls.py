from rest_framework.routers import SimpleRouter
from django.urls import path

from workplace.views import ShopViewSet, ShopProducts

router = SimpleRouter()

router.register("shop", ShopViewSet, "shop")

urlpatterns = router.urls
urlpatterns += [path("shop/<slug>/products/", ShopProducts.as_view())]
