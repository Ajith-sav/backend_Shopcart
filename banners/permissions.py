from rest_framework import permissions


class IsStaffAndSelf(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True

        if request.method == "POST":
            return request.user.role == "admin"

        if request.method == "DELETE":
            return request.user.role == "admin"

        if not request.user or not request.user.is_authenticated:
            return False

        if getattr(request.user, "role", None) != "staff":
            return False

        return True

    def has_object_permission(self, request, view, obj):

        if request.method in ["POST", "PUT"]:
            return obj.staff_id == request.user.id

        return True
