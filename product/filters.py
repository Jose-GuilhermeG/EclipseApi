import django_filters as filters
from .models import Product

class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price" , lookup_expr="gt")
    max_price = filters.NumberFilter(field_name="price" , lookup_expr="lt")
    evaluation = filters.NumberFilter(field_name='evaluations__rating' , lookup_expr='exact' )
    
    class Meta:
        model = Product
        fields = ['max_price' , 'min_price' , 'categorys']