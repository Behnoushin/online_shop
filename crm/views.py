from rest_framework import generics
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from product.models import Product, Category
from product.serializers import ProductSerializer, CategorySerializer
from datetime import datetime, timedelta
from user_management.models import CustomUser, PurchaseHistory
from django.db.models import Sum, Count, Avg


class ProductUpdate(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

class CategoryListUpdate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

class AdminDashboardDataView(RetrieveAPIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        now = datetime.now()
        last_24_hours = now - timedelta(hours=24)
        last_7_days = now - timedelta(days=7)
        

        data = {
            "total_number_of_users": CustomUser.objects.count(),
            "total_number_of_orders": PurchaseHistory.objects.count(),
            "revenue": PurchaseHistory.objects.aggregate(Sum('product__price'))['product__price__sum'] or 0,
            "number_of_products": Product.objects.count(),
            "out_of_stock_products": Product.objects.filter(stock=0).count(),
            "new_users_this_month": CustomUser.objects.filter(date_joined__month=now.month).count(),
            "orders_placed_today": PurchaseHistory.objects.filter(purchase_date__gte=last_24_hours).count(),
            "most_sold_products": PurchaseHistory.objects.values('product__title').annotate(sales_count=Sum('quantity')).order_by('-sales_count')[:5],
            "orders_by_status": PurchaseHistory.objects.values('status').annotate(count=Count('id')),
            "average_order_value": PurchaseHistory.objects.aggregate(Avg('product__price'))['product__price__avg'] or 0,
            "best_customers": CustomUser.objects.annotate(order_count=Count('purchasehistory')).order_by('-order_count')[:5],
            "revenue_breakdown_by_month": PurchaseHistory.objects.filter(purchase_date__year=now.year).extra(select={'month': 'EXTRACT(MONTH FROM purchase_date)'}).values('month').annotate(total_revenue=Sum('product__price')),
            "low_stock_products": Product.objects.filter(stock__lt=10).count(),
            "new_products_added_this_week": Product.objects.filter(created_at__gte=last_7_days).count(),
        }
        return Response(data)

