import django_filters as filters
from .models import Product , Category , Evaluation , Doubt

class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price" , lookup_expr="gt")
    max_price = filters.NumberFilter(field_name="price" , lookup_expr="lt")
    evaluation = filters.NumberFilter(field_name='evaluations__rating' , lookup_expr='exact' )
    
    class Meta:
        model = Product
        fields = ['max_price' , 'min_price' , 'categorys']
        
class CategoryFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    
    class Meta:
        model = Category
        fields = ['name']
        
class EvaluationFilter(filters.FilterSet):
    class Meta: 
        model = Evaluation
        fields = ['rating']
        
class DoubtFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    created_at = filters.DateTimeFilter()
    class Meta:
        model = Doubt
        fields = ['created_at','title']