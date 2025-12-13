# imports
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from core.mixins import (
    ViewSetAddPermissionsMixin,
    ViewSetGetSerializerClassMixin,
    SetCache,
)

# models
from workplace.models import Shop

# serializes
from workplace.serializers import ShopListSerializer, ShopDetailSerializer

# filters

# permissions
from workplace.permissions import IsShopOwner


# views
class ShopViewSet(
    ViewSetGetSerializerClassMixin, ViewSetAddPermissionsMixin, SetCache, ModelViewSet
):

    queryset = Shop.objects.all()
    lookup_field = "slug"
    serializers_class_per_action = {
        "list": ShopListSerializer,
        "create": ShopDetailSerializer,
        "update": ShopDetailSerializer,
        "retrieve": ShopDetailSerializer,
        "partial_update": ShopDetailSerializer,
    }

    permissions_class_per_action = {
        "create": IsAuthenticated,
        "update": IsShopOwner,
        "partial_update": IsShopOwner,
        "destroy": IsShopOwner,
    }

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
