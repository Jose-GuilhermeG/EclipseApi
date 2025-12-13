#imports
from rest_framework import serializers
from .models import Product , Category , Evaluation , Doubt
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse

USER = get_user_model() 

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id' ,'name' , 'image' , 'price' , 'slug']
        
class ProductDetailSerializer(serializers.ModelSerializer):
    categorys = serializers.StringRelatedField(many=True)
    rating = serializers.FloatField(source='get_rating')
    evaluations = serializers.IntegerField(source='get_evaluations_number')
    rating_count = serializers.SerializerMethodField()
    shop = serializers.CharField()
    
    class Meta:
        model = Product
        exclude = ['id' , 'updated_at' , 'updated_by' , 'is_active' , 'created_by']
        
    def get_evaluations_url(self , obj ):
        return reverse('product:evaluations-list' , kwargs={'slug' : obj.slug})
    
    def get_rating_count(self,obj):
        return obj.evaluations.count()
        
class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name' , 'price' , 'description' , 'image' , 'categorys']
        depht = 1
    
class CategoryListSerializer(serializers.ModelSerializer):
    category_url = serializers.HyperlinkedIdentityField(
        view_name = 'product:category-detail',
        lookup_field = 'slug',
    )
    slug = serializers.CharField(read_only=True)
    class Meta:
        model = Category
        fields = ['name' , 'slug' , 'category_url']
        
class CategoryProductSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(many=True)
    class Meta:
        model = Category
        fields = ['name' , 'product']
        
class ProductEvaluation(serializers.HyperlinkedModelSerializer):
    user = serializers.CharField(read_only=True)
    user_photo = serializers.ImageField(source='user.photo',read_only = True)
    url = serializers.CharField(source='get_absolute_url',read_only=True)
    class Meta:
        model = Evaluation
        fields = ['url','user','user_photo','rating','comment']
        
        
class DoubCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doubt
        fields = ['title' , 'content']
        
class ProductDoubSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    user_photo = serializers.ImageField(source='user.photo',read_only = True)
    url = serializers.CharField(source='get_absolute_url',read_only=True)
    created_at = serializers.DateTimeField(format='%d-%m-%Y' , read_only=True)
    
    class Meta:
        model = Doubt
        fields = ['user','user_photo','url','title','created_at']
        
class ProductDoubEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doubt
        fields = ['title' , 'content']