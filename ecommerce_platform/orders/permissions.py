from rest_framework import permissions

class IsCustomerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.customer.user == request.user

