#imports
from rest_framework.viewsets import ModelViewSet 
from rest_framework import generics
from django.contrib.auth import get_user_model
from core.mixins import ViewSetAddPermissionsMixin , get_access_and_refresh_tokens , ViewSetGetSerializerClassMixin , ViewSetAddDefaultPermissionMixin
from django.utils.translation import gettext_lazy as _
from core.utils import create_view_schema , create_viewset_schema

#models
USER = get_user_model()

#serializes
from users import serializers

#filters

#permissions
from rest_framework.permissions import IsAuthenticated , IsAdminUser

schema = create_viewset_schema("shopping car")

#views
@schema
class UserShppingCarViewSet(
    ViewSetAddDefaultPermissionMixin,
    ViewSetGetSerializerClassMixin,
    ModelViewSet
):
    default_permisson = [IsAuthenticated]
    http_method_names = ['get','post','delete','put']
    serializers_class_per_action = {
        'list' : serializers.ShoppingCarItemsSerializer ,
        'create' : serializers.ShoppingCarItemCreateSerializer,
        'update' : serializers.ShoppingCarItemCreateSerializer,
        'retrieve' : serializers.ShoppingCarItemSerializer,
    }
    
    def get_queryset(self):
        return self.request.user.shopping_car.items.all()
    
    def perform_create(self, serializer):
        return serializer.save(
            shopping_car = self.request.user.shopping_car
        )