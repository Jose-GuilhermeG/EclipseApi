from django.urls import path
from rest_framework.routers import SimpleRouter

from workplace.views import ShopViewSet

router = SimpleRouter()

router.register(
    'shop',
    ShopViewSet,
    'shop'
)

urlpatterns = router.urls
