from rest_framework.permissions import BasePermission


class IsTravelerOrAuhenticated(BasePermission):
    def has_permission(self, request, permission):
        if request.method == 'GET':
                return True
        return bool(request.user and request.user.is_authenticated)


    
class IsSellerLocations(BasePermission):
    def has_permission(self, request, permission):
        if bool(request.user and request.user.is_authenticated):
            if request.method == 'GET':
                    return True
            return request.user.is_staff or request.user.is_seller
        return False