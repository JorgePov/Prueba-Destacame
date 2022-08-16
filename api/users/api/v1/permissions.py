from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, permission):
        if request.method == 'GET':
            return True
        return request.user.is_staff