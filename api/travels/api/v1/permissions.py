from rest_framework.permissions import BasePermission


class IsAdminAndReadOnly(BasePermission):
    def has_permission(self, request, permission):
        if bool(request.user and request.user.is_authenticated):
            if request.method == 'GET':
                return True
            return request.user.is_staff
        return False
