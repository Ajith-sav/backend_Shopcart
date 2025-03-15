from rest_framework.permissions import BasePermission


class OrderPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.role == "customer"
