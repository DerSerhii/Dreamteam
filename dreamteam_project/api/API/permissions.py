from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    """
    Allows access only to manage members.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_manager)
