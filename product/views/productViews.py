# imports
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from core.mixins import (
    AddCreatedByMixin,
    ViewSetAddPermissionsMixin,
    ViewSetGetSerializerClassMixin,
    SetCache,
)
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from core.constants import DEFAULT_CACHE_TIME

# models
from product.models import Product

# serializes
from product import serializers

# filters
from product.filters import ProductFilter

# permissions
from product.permissions import IsProductOwner


# views
class ProductViewSet(
    ViewSetAddPermissionsMixin,
    ViewSetGetSerializerClassMixin,
    AddCreatedByMixin,
    SetCache,
    ModelViewSet,
):
    queryset = Product.objects.all()
    lookup_field = "slug"
    filterset_class = ProductFilter
    permissions_class_per_action = {
        "create": IsAuthenticated,
        "update": IsProductOwner,
        "partial_update": IsProductOwner,
        "destroy": IsProductOwner,
    }
    serializers_class_per_action = {
        "list": serializers.ProductListSerializer,
        "create": serializers.ProductCreateSerializer,
        "update": serializers.ProductCreateSerializer,
        "retrieve": serializers.ProductDetailSerializer,
        "partial_update": serializers.ProductCreateSerializer,
        "feature": serializers.ProductListSerializer,
    }

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(methods=["get"], detail=False, url_path="feature")
    @method_decorator(cache_page(DEFAULT_CACHE_TIME))
    def feature(self, *args):
        instance = Product.objects.order_by("-views").first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ProductSearchView(SetCache, generics.ListAPIView):
    serializer_class = serializers.ProductListSerializer
    filterset_class = ProductFilter

    def get_queryset(self):
        query = self.kwargs.get("query")
        return Product.objects.search(query)
