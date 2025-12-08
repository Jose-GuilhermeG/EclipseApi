#imports
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from core.mixins import AddCreatedByMixin , ViewSetAddPermissionsMixin , ViewSetGetSerializerClassMixin , SetCache

#models
from product.models import Product

#serializes
from product import serializers

#filters
from product.filters import ProductFilter

#permissions
from product.permissions import IsObjOwner , IsObjUser


#views
class ProductViewSet(
    ViewSetAddPermissionsMixin,
    ViewSetGetSerializerClassMixin,
    AddCreatedByMixin,
    SetCache,
    ModelViewSet
):
    queryset = Product.objects.all()
    lookup_field = 'slug'
    filterset_class = ProductFilter
    permissions_class_per_action = {
            'create' :  IsAuthenticated,
            'update' : IsObjOwner,
            'partial_update' : IsObjOwner,
            'destroy' : IsObjOwner
    }
    serializers_class_per_action = {
        'list' : serializers.ProductListSerializer,
        'create' :  serializers.ProductCreateSerializer,
        'update' : serializers.ProductCreateSerializer,
        'retrieve' : serializers.ProductDetailSerializer,
        'partial_update' : serializers.ProductCreateSerializer,
        'search' : serializers.ProductListSerializer,
    }
    
    
class ProductSearchView(
    SetCache,
    generics.ListAPIView
):
    serializer_class = serializers.ProductListSerializer
    
    def get_queryset(self):
        query = self.kwargs.get('query')
        return Product.objects.search(query)

    
class ProductFeatureView(generics.RetrieveAPIView):
    serializer_class = serializers.ProductListSerializer
    
    def get_object(self):
        return Product.objects.get(slug='airpods-max')
        