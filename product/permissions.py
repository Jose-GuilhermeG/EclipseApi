from rest_framework.permissions import BasePermission


class IsProductOwner(BasePermission):
    """
    Permission class to check if the user is the owner of the product.
    """

    def has_permission(self, request, view):
        return request.user

    def has_object_permission(self, request, view, obj):
        return obj.shop.id == request.user.shop.id


class IsObjUser:
    """
    Permission class to check if the user is same of obj field user
    """

    def has_permission(self, request, view):
        return request.user

    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id
