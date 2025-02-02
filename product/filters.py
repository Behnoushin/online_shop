from django_filters import rest_framework as filters
from .models import Product , Brand

class ProductFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    category = filters.CharFilter(field_name="category__name", lookup_expr="icontains")
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    warranty_start_date = filters.DateFilter(field_name="warranty__start_date", lookup_expr="gte")
    warranty_end_date = filters.DateFilter(field_name="warranty__end_date", lookup_expr="lte")
    cheapest = filters.BooleanFilter(method='filter_cheapest')
    most_expensive = filters.BooleanFilter(method='filter_most_expensive')
    newest = filters.BooleanFilter(method='filter_newest')
    related = filters.BooleanFilter(method='filter_related')

    class Meta:
        model = Product
        fields = "__all__"

    def filter_cheapest(self, queryset, name, value):
        if value:
            return queryset.order_by('price') 
        return queryset

    def filter_most_expensive(self, queryset, name, value):
        if value:
            return queryset.order_by('-price') 
        return queryset
    
    def filter_newest(self, queryset, name, value):
        if value:
            return queryset.order_by('-created_at')  
        return queryset
    
    def filter_related(self, queryset, name, value):
        category = self.filters.get('category')
        if category:
            return queryset.filter(category=category)
        return queryset


class BrandFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")  
    country = filters.CharFilter(field_name="country", lookup_expr="icontains") 
    image = filters.CharFilter(field_name="image", lookup_expr="icontains") 
    created_after = filters.DateFilter(field_name="created_at", lookup_expr="gte")
    created_before = filters.DateFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Brand
        fields = "__all__"