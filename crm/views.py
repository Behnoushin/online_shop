from rest_framework import generics
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from product.models import Product, Category, Review, Rating, Coupon
from product.serializers import ProductSerializer, CategorySerializer
from user_management.models import CustomUser, PurchaseHistory
from user_management.serializers import UserSerializer
from order.models import Order, OrderItem, Payment
from shipping.models import Shipment
from utility.views import SoftDeleteGenericView

from datetime import datetime, timedelta
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
            # Total counts of users, orders, and products
            "total_number_of_users": CustomUser.objects.count(),
            "total_number_of_products": Product.objects.count(),

            # Revenue and product statistics
            "revenue": PurchaseHistory.objects.aggregate(Sum('product__price'))['product__price__sum'] or 0,
            "out_of_stock_products": Product.objects.filter(stock=0).count(),
            "low_stock_products": Product.objects.filter(stock__lt=10).count(),
            "new_products_added_this_week": Product.objects.filter(created_at__gte=last_7_days).count(),

            # New users and orders statistics
            "new_users_this_month": CustomUser.objects.filter(date_joined__month=now.month).count(),
            "orders_placed_today_purchase_history": PurchaseHistory.objects.filter(purchase_date__gte=last_24_hours).count(),
            "orders_placed_today_orders": Order.objects.filter(created_at__gte=last_24_hours).count(),

            # Most sold products (based on PurchaseHistory and OrderItem)
            "most_sold_products_purchase_history": PurchaseHistory.objects.values('product__title').annotate(sales_count=Sum('quantity')).order_by('-sales_count')[:5],
            "most_sold_products_this_week_purchase_history": PurchaseHistory.objects.filter(purchase_date__gte=last_7_days).values('product__title').annotate(sales_count=Sum('quantity')).order_by('-sales_count')[:5],
            "most_sold_products_this_week_orders": OrderItem.objects.filter(order__created_at__gte=last_7_days).values('product__title').annotate(sales_count=Sum('quantity')).order_by('-sales_count')[:5],

            # Orders and statuses
            "orders_by_status_purchase_history": PurchaseHistory.objects.values('status').annotate(count=Count('id')),
            "orders_by_status_orders": Order.objects.values('status').annotate(count=Count('id')),

            # Average order values
            "average_order_value_purchase_history": PurchaseHistory.objects.aggregate(Avg('product__price'))['product__price__avg'] or 0,
            "average_order_value_orders": Order.objects.aggregate(Avg('total_amount'))['total_amount__avg'] or 0,

            # Best customers and single product orders
            "best_customers": CustomUser.objects.annotate(order_count=Count('purchasehistory')).order_by('-order_count')[:5],
            "single_product_orders": PurchaseHistory.objects.filter(quantity=1).count(),

            # Product ratings and reviews
            "average_product_rating": Product.objects.annotate(avg_rating=Avg('ratings__score')).values('id', 'avg_rating'),
            "total_number_of_reviews": Review.objects.count(),
            "total_ratings": Rating.objects.count(),

            # Average orders per user
            "average_orders_per_user": PurchaseHistory.objects.values('user').annotate(order_count=Count('id')).aggregate(Avg('order_count'))['order_count__avg'] or 0,

            # Coupon statistics
            "total_coupons_used": Coupon.objects.filter(used_count__gt=0).count(),
            "most_used_coupon": Coupon.objects.annotate(usage_count=Sum('used_count')).order_by('-usage_count').first(),

            # Users with highest discounts
            "users_with_highest_discounts": CustomUser.objects.annotate(total_discount=Sum('purchasehistory__product__highest_discount')).order_by('-total_discount')[:5],

            # Revenue and shipment statistics
            "total_revenue": Payment.objects.aggregate(Sum('final_amount'))['final_amount__sum'] or 0,
            "total_shipment_count": Shipment.objects.count(),
            "most_used_shipping_method": Shipment.objects.values('shipping_method__name').annotate(count=Count('id')).order_by('-count').first(),
        }
        return Response(data)


class ProductDeleteView(SoftDeleteGenericView):
    queryset = Product.objects.filter(is_deleted=False)
    serializer_class = ProductSerializer 
    permission_classes = [IsAdminUser]


class UserProfileDeleteView(SoftDeleteGenericView):
    queryset = CustomUser.objects.filter(is_deleted=False)
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
