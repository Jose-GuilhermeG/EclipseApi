# imports
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from core.mixins import (
    AddCreatedByMixin,
    ViewSetAddPermissionsMixin,
    ViewSetGetSerializerClassMixin,
    SetCache,
)

# models
from product.models import Category

# serializes
from product import serializers

# filters
from product.filters import CategoryFilter

# permissions


# views
class CategoryViewSet(
    ViewSetGetSerializerClassMixin,
    ViewSetAddPermissionsMixin,
    AddCreatedByMixin,
    SetCache,
    ModelViewSet,
):
    queryset = Category.objects.all()
    lookup_field = "slug"
    permissions_class_per_action = {
        "create": IsAdminUser,
        "update": IsAdminUser,
        "partial_update": IsAdminUser,
        "destroy": IsAdminUser,
    }

    serializers_class_per_action = {
        "list": serializers.CategoryListSerializer,
        "create": serializers.CategoryListSerializer,
        "update": serializers.CategoryListSerializer,
        "retrieve": serializers.CategoryProductSerializer,
        "partial_update": serializers.CategoryListSerializer,
    }
    filterset_class = CategoryFilter
