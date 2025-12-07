#imports
from rest_framework.viewsets import ModelViewSet 
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from core.mixins import ViewSetAddPermissionsMixin , get_access_and_refresh_tokens , ViewSetGetSerializerClassMixin , ViewSetAddDefaultPermissionMixin
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page


from users import serializers
from users import models


USER = get_user_model()

# Create your views here.
class UserViewSet(
    ViewSetAddPermissionsMixin,  
    ViewSetGetSerializerClassMixin, 
    ModelViewSet,
):
    queryset = USER.objects.all()
    permissions_classes = {
        'list' :  IsAdminUser,
        'update' : IsAuthenticated,
        'partial_update' : IsAuthenticated,
        'destroy' : IsAuthenticated
    }       

    serializers_classes = {
            'list' : serializers.UserSerializer,
            'update' : serializers.UserSerializer,
            'retrieve' : serializers.UserSerializer,
            'partial_update' : serializers.UserSerializer,
            'change_password' : serializers.SetPasswordSerializer
    }
        

    def get_object(self):
        return get_object_or_404(USER , pk = self.request.user.pk)
        
class RegisterView(
    generics.CreateAPIView
):
    queryset = USER.objects.all()
    serializer_class = serializers.RegisterSerializer
    
    def perform_create(self, serializer):
        self.object = serializer.save()
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.data = get_access_and_refresh_tokens.get_tokens_for_user(self.object)
        return response
    
class ChangePasswordView(
    generics.UpdateAPIView
):
    queryset = USER.objects.all()
    serializer_class = serializers.SetPasswordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return get_object_or_404(USER , pk = self.request.user.pk)
    
    def perform_update(self, serializer):
        serializer.save()
        
    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        response.data = {'detail' : 'Password changed successfully.'}
        return response

class UserShopingCarItensListView(
    generics.ListCreateAPIView
):
    permission_class = [IsAuthenticated]
    
    #temporario , criar mixin para reutilizar logica
    def get_serializer_class(self):
        serializer = None
        serializer_class = {'GET' : serializers.ShoppingCarItemsSerializer , "POST" : serializers.ShoppingCarItemCreateSerializer }
        return serializer_class[self.request.method]
    
    def get_queryset(self):
        return self.request.user.shopping_car.items.all()
    
    def perform_create(self, serializer):
        return serializer.save(
            shopping_car = self.request.user.shopping_car
        )
        
class UserPurchasedList(
    generics.ListCreateAPIView
):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return models.Purchased.objects.filter(user = self.request.user)
    
    #temporario , criar mixin para reutilizar logica
    def get_serializer_class(self):
        serializer = None
        serializer_class = {'GET' : serializers.PurchasedListSerializer , "POST" : serializers.PurchasedCreateSerializer }
        return serializer_class[self.request.method]
    
    def perform_create(self, serializer):
        return serializer.save(
            user = self.request.user
        )