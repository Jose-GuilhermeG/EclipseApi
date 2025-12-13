# imports
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from django.contrib.auth import get_user_model
from core.mixins import (
    ViewSetAddPermissionsMixin,
    get_access_and_refresh_tokens,
    ViewSetGetSerializerClassMixin,
)
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _


# serializes
from users import serializers

# filters

# permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# models
USER = get_user_model()


# mixins
class getUSer:
    def get_object(self):
        return get_object_or_404(USER, pk=self.request.user.pk)


# views
class UserViewSet(
    ViewSetAddPermissionsMixin,
    ViewSetGetSerializerClassMixin,
    getUSer,
    ModelViewSet,
):
    queryset = USER.objects.all()
    permissions_class_per_action = {
        "list": IsAdminUser,
        "update": IsAuthenticated,
        "partial_update": IsAuthenticated,
        "destroy": IsAuthenticated,
    }

    serializers_class_per_action = {
        "list": serializers.UserSerializer,
        "update": serializers.UserSerializer,
        "retrieve": serializers.UserSerializer,
        "partial_update": serializers.UserSerializer,
        "change_password": serializers.SetPasswordSerializer,
    }


class RegisterView(generics.CreateAPIView):
    queryset = USER.objects.all()
    serializer_class = serializers.RegisterSerializer

    def perform_create(self, serializer):
        self.object = serializer.save()

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.data = get_access_and_refresh_tokens.get_tokens_for_user(self.object)
        return response


class ChangePasswordView(getUSer, generics.UpdateAPIView):
    queryset = USER.objects.all()
    serializer_class = serializers.SetPasswordSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        response.data = {"detail": _("Password changed successfully.")}
        return response
