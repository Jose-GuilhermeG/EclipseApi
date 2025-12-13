#imports
from rest_framework import serializers

#models
from workplace.models import Shop

#serializers
class ShopListSerializer(
    serializers.ModelSerializer
):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name = 'workplace:shop-detail',
        lookup_field = 'slug'
    )
    
    class Meta:
        model = Shop
        fields = ['name','slug','photo','detail_url']
        
class ShopDetailSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = Shop
        fields = ['name' ,'description', 'photo' , 'banner' , 'created_at']
        extra_kwargs = {'read_only' : ['created_at']}