from rest_framework import permissions
from .models import Payment

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Allows the user to only view their own payments and only admins are allowed to make changes.
    """

    def has_permission(self, request, view):
        return request.method == 'GET' or request.user.is_staff or self.is_owner(request, view)

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.order.user == request.user

    def is_owner(self, request, view):
        if not request.user.is_authenticated:
            return False  
    
        payment_id = view.kwargs.get('pk')  
        if not payment_id:
            return False 

        return Payment.objects.filter(pk=payment_id, order__user=request.user).exists()
