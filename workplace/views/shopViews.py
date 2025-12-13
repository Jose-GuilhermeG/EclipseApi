#imports
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from core.mixins import AddCreatedByMixin , ViewSetAddPermissionsMixin , ViewSetAddDefaultPermissionMixin , ViewSetGetSerializerClassMixin , SetCache
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from core.constants import DEFAULT_CACHE_TIME

#models
from workplace.models import Shop

#serializes
from workplace.serializers import ShopListSerializer , ShopDetailSerializer

#filters

#permissions
from workplace.permissions import IsShopOwner
from rest_framework.permissions import IsAuthenticated

#views
class ShopViewSet(
    ViewSetGetSerializerClassMixin,
    ViewSetAddPermissionsMixin,
    SetCache,
    ModelViewSet
):

    queryset = Shop.objects.all()
    lookup_field = 'slug'
    serializers_class_per_action = {
        'list' : ShopListSerializer,
        'create' :  ShopDetailSerializer,
        'update' : ShopDetailSerializer,
        'retrieve' : ShopDetailSerializer,
        'partial_update' : ShopDetailSerializer,
    }
    
    permissions_class_per_action = {
        'create' : IsAuthenticated,
        'update' : IsShopOwner,
        'partial_update' : IsShopOwner,
        'destroy' : IsShopOwner,
    }
    
    def perform_create(self, serializer):
        serializer.save(
            owner = self.request.user
        )