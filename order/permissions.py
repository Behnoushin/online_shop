from rest_framework import permissions
from .models import Payment

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Allows the user to only view their own payments and only admins are allowed to make changes.
    """

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.user.is_staff:
            return True 
        if request.user.is_authenticated and view.kwargs.get('pk'):
            payment = Payment.objects.get(pk=view.kwargs['pk'])
            return payment.order.user == request.user 
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.order.user == request.user 
