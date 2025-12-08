#imports
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from core.utils import create_view_schema

#models
from product.models import Product , Doubt

#serializes
from product import serializers

#filters
from product.filters import DoubtFilter

#permissions
from product.permissions import IsObjOwner

#schema
schema_name = "doubts"

#mixins
class GetDoubtByProduct:
    def get_product(self):
        slug = self.kwargs.get("slug")
        return get_object_or_404(Product , slug = slug)
    
    def get_object(self):
        slug = self.kwargs.get("slug")
        id = self.kwargs.get("id")
        return get_object_or_404(Doubt , product__slug = slug , id=id)
    
    def get_queryset(self):
        slug = self.kwargs.get("slug")
        return Doubt.objects.filter(product__slug = slug)

#views
@create_view_schema(schema_name,['get','post'])
class ProducDoubtListCreateView(
    GetDoubtByProduct,
    generics.ListCreateAPIView,
):
    serializer_class = serializers.ProductDoubSerializer
    filterset_class = DoubtFilter
    #refatorar
    permission_classes = [IsAuthenticated]

    def perform_create(self , serializer):
        serializer.save(
            created_by = self.request.user,
            user = self.request.user,
            product = self.get_product()
        )

@create_view_schema(schema_name,['delete','put','get','patch'])
class ProductDoubtUpdateDeleteView(
    GetDoubtByProduct,
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = serializers.ProductDoubEditSerializer
    permission_classes = [IsObjOwner]
    lookup_field = 'id'