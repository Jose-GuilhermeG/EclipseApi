# imports
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from core.mixins import ViewSetGetSerializerClassMixin, ViewSetAddDefaultPermissionMixin
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from core.utils import create_viewset_schema

# serializes
from users import serializers

# filters

# permissions
from rest_framework.permissions import IsAuthenticated

# models
from users.models import Purchased
from users.enuns import PURCHASEDSTATUS

USER = get_user_model()


# views
@create_viewset_schema("purchased")
class UserPurchasedViewset(
    ViewSetAddDefaultPermissionMixin, ViewSetGetSerializerClassMixin, ModelViewSet
):
    default_permission = [IsAuthenticated]
    http_method_names = ["get", "post"]
    serializers_class_per_action = {
        "list": serializers.PurchasedListSerializer,
        "create": serializers.PurchasedCreateSerializer,
        "retrieve": serializers.PurchasedDetailSerializer,
    }

    def get_queryset(self):
        return Purchased.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_object(self):
        return get_object_or_404(
            Purchased, user=self.request.user, id=self.kwargs.get("id")
        )


@extend_schema(tags=["purchased"])
@api_view(["post"])
@permission_classes([IsAuthenticated])
def confirm_delivered(request, id):
    purchased_obj = get_object_or_404(Purchased, user=request.user, id=id)
    delivered_status = PURCHASEDSTATUS.DELIVERED

    if purchased_obj.status == delivered_status:
        return Response(
            {"err": _("purchased delivered")}, status=status.HTTP_400_BAD_REQUEST
        )

    purchased_obj.status = delivered_status
    purchased_obj.save()
    return Response({"confirm_delivered": True}, status=status.HTTP_200_OK)
