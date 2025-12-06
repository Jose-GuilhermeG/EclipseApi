#imports
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


from core.mixins import AddCreatedByMixin , ViewSetAddPermissionsMixin , ViewSetGetSerializerClassMixin , SetCache
from .models import Product , Category , Evaluation , Doubt
from .permissions import IsObjOwner , IsObjUser
from product import serializers
from .filters import ProductFilter

# Create your views here.
class ProductView(
    ViewSetAddPermissionsMixin,
    ViewSetGetSerializerClassMixin,
    AddCreatedByMixin,
    SetCache,
    ModelViewSet
):
    queryset = Product.objects.all()
    lookup_field = 'slug'
    filterset_class = ProductFilter
    permissions_classes = {
            'create' :  IsAuthenticated,
            'update' : IsObjOwner,
            'partial_update' : IsObjOwner,
            'destroy' : IsObjOwner
    }
    serializers_classes = {
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
        
    
class CategoryViewSet(
    ViewSetGetSerializerClassMixin,
    ViewSetAddPermissionsMixin,
    AddCreatedByMixin,
    SetCache,
    ModelViewSet
):
    queryset = Category.objects.all()
    lookup_field = 'slug'
    permissions_classes = {
            'create' :  IsAdminUser,
            'update' : IsAdminUser,
            'partial_update' : IsAdminUser,
            'destroy' : IsAdminUser
    }
    
    serializers_classes = {
        'list' : serializers.CategoryListSerializer,
        'create' :  serializers.CategoryListSerializer,
        'update' : serializers.CategoryListSerializer,
        'retrieve' : serializers.CategoryProductSerializer,
        'partial_update' : serializers.CategoryListSerializer,
    }
    
class ProductEvaluationView(
    ViewSetAddPermissionsMixin,
    ModelViewSet,
):
    
    permissions_classes = {
       "create" : IsAuthenticated,
       "destroy" : IsObjUser,
       "update" : IsObjUser,
    }    
    
    serializer_class = serializers.ProductEvaluation
    
    def get_queryset(self):
        slug = self.kwargs.get("slug")
        return Evaluation.objects.filter(product__slug = slug)
    
    def get_object(self)->Evaluation:
        slug = self.kwargs.get("slug")
        pk = self.kwargs.get("pk")
        return get_object_or_404(Evaluation , product__slug = slug , pk=pk)
    
    def get_product(self)->Product:
        slug = self.kwargs.get("slug")
        return get_object_or_404(Product , slug = slug)
 
    def perform_create(self , serializer)->None:
        serializer.save(
            created_by = self.request.user,
            user = self.request.user,
            product = self.get_product()
        )
        
class ProductEvaluationUpdateDeleteView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = serializers.ProductEvaluation
    permission_classes = [IsObjOwner]
    lookup_field = 'id'
    
    def get_object(self):
        slug = self.kwargs.get("slug")
        id = self.kwargs.get("id")
        return get_object_or_404(Evaluation , product__slug = slug , id=id)
    
class ProducDoubtListView(generics.ListAPIView):
    serializer_class = serializers.ProductDoubSerializer
    
    def get_queryset(self):
        slug = self.kwargs.get("slug")
        return Doubt.objects.filter(product__slug = slug)
    
class ProductDoubtCreateView(generics.CreateAPIView):
    serializer_class = serializers.DoubCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        slug = self.kwargs.get("slug")
        return get_object_or_404(Product , slug = slug)
 
    def perform_create(self , serializer):
        serializer.save(
            created_by = self.request.user,
            user = self.request.user,
            product = self.get_object()
        )
        
class ProductDoubtUpdateDeleteView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = serializers.ProductDoubEditSerializer
    permission_classes = [IsObjOwner]
    lookup_field = 'id'
    
    def get_object(self):
        slug = self.kwargs.get("slug")
        id = self.kwargs.get("id")
        return get_object_or_404(Doubt , product__slug = slug , id=id)