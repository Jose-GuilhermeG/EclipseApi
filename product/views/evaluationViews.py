# imports
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from core.mixins import ViewSetAddPermissionsMixin
from django.shortcuts import get_object_or_404
from core.utils import create_viewset_schema

# models
from product.models import Product, Evaluation

# serializes
from product import serializers

# filters
from product.filters import EvaluationFilter

# permissions
from product.permissions import IsObjUser

# schema
schema = create_viewset_schema("evaluations")

# views


@schema
class ProductEvaluationViewSet(
    ViewSetAddPermissionsMixin,
    ModelViewSet,
):

    permissions_class_per_action = {
        "create": IsAuthenticated,
        "destroy": IsObjUser,
        "update": IsObjUser,
    }

    serializer_class = serializers.ProductEvaluation
    filterset_class = EvaluationFilter

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        return Evaluation.objects.filter(product__slug=slug)

    def get_object(self) -> Evaluation:
        slug = self.kwargs.get("slug")
        pk = self.kwargs.get("pk")
        return get_object_or_404(Evaluation, product__slug=slug, pk=pk)

    def get_product(self) -> Product:
        slug = self.kwargs.get("slug")
        return get_object_or_404(Product, slug=slug)

    def perform_create(self, serializer) -> None:
        serializer.save(
            created_by=self.request.user,
            user=self.request.user,
            product=self.get_product(),
        )
