from rest_framework.permissions import BasePermission


class IsSuperUserPermission(BasePermission):
    message = 'Only admin is allowed to preform this action'
    def has_permission(self, request, view):
        return request.user.is_superuser