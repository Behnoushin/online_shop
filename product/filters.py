from django_filters import rest_framework as filters
from .models import Product , Brand

class ProductFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    category = filters.CharFilter(field_name="category__name", lookup_expr="icontains")
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Product
        fields = ['title', 'category', 'min_price', 'max_price']

class BrandFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")  
    country = filters.CharFilter(field_name="country", lookup_expr="icontains") 
    image = filters.CharFilter(field_name="image", lookup_expr="icontains") 

    class Meta:
        model = Brand
        fields = ['name', 'country', 'image']