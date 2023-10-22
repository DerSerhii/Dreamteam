from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsManager(BasePermission):
    """
    Allows access only to manage members.
    """

    def has_permission(self, request, view):
        return request.user.is_manager


class IsManagerOrReadOnlyOwnProfile(BasePermission):
    """
    """

    def has_permission(self, request, view):
        return request.user.is_manager or view.action == 'retrieve'

    def has_object_permission(self, request, view, obj):
        # Non-managers can only access their own member object.
        return request.user.is_manager or obj == request.user


class IsManagerOrReadOnlyOwnTeam(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_manager or view.action == 'retrieve'

    def has_object_permission(self, request, view, obj):
        return request.user.is_manager or obj.members.filter(id=request.user.id).exists()
