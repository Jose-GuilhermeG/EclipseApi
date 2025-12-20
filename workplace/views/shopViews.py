# imports
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from core.mixins import (
    ViewSetAddPermissionsMixin,
    ViewSetGetSerializerClassMixin,
    SetCache,
)
from django.shortcuts import get_object_or_404
from rest_framework import generics

# models
from workplace.models import Shop

# serializes
from workplace.serializers import ShopListSerializer, ShopDetailSerializer
from product.serializers import ProductListSerializer

# filters
from product.filters import ProductFilter

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


class ShopProducts(generics.ListAPIView):
    serializer_class = ProductListSerializer
    filterset_class = ProductFilter
    lookup_url_kwarg = "slug"
    kwargs = ["slug"]

    def get_queryset(self):
        shop = get_object_or_404(Shop, slug=self.kwargs.get("slug"))
        return shop.products.all()
