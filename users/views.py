#imports
from rest_framework.viewsets import ModelViewSet 
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from core.mixins import ViewSetAddPermissionsMixin , get_access_and_refresh_tokens , ViewSetGetSerializerClassMixin , ViewSetAddDefaultPermissionMixin
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page


from users.serializers import RegisterSerializer , UserSerializer , AuthenticationSerializer , SetPasswordSerializer , ShoppingCarItemCreateSerializer , ShoppingCarItemsSerializer
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
            'list' : UserSerializer,
            'update' : UserSerializer,
            'retrieve' : UserSerializer,
            'partial_update' : UserSerializer,
            'change_password' : SetPasswordSerializer
    }
        

    def get_object(self):
        return get_object_or_404(USER , pk = self.request.user.pk)
        
class RegisterView(
    generics.CreateAPIView
):
    queryset = USER.objects.all()
    serializer_class = RegisterSerializer
    
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
    serializer_class = SetPasswordSerializer
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
    
    def get_serializer_class(self):
        serializer = None
        serializer_class = {'GET' : ShoppingCarItemsSerializer , "POST" : ShoppingCarItemCreateSerializer }
        return serializer_class[self.request.method]
    
    def get_queryset(self):
        return self.request.user.shopping_car.items.all()
    
    def perform_create(self, serializer):
        return serializer.save(
            shopping_car = self.request.user.shopping_car
        )