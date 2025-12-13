#imports
from rest_framework.permissions import BasePermission

#permissions
class IsShopOwner(
    BasePermission
):
    
    def has_permission(self, request, view):
        return request.user
    
    def has_object_permission(self, request, view, obj):
        return obj.owner.id == request.user.id