from rest_framework import permissions

class ReadOnlyForAllButAdmin(permissions.BasePermission):
    """
    All users (even unauthenticated ones) can view the data,
    but only admins are allowed to create, update, or delete.
    """
    def has_permission(self, request, view):
        # Allow all GET (read-only) requests
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only admins can modify the data
        return request.user.is_authenticated and request.user.is_staff

