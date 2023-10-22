"""
The module represents CUSTOM PERMISSION classes used in the project.
"""

from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    """
    Custom permission class for checking if a user is a manager.

    This permission class allows access only to members
    with the `is_manager` attribute set to `True`.
    """

    def has_permission(self, request, view) -> bool:
        """
        Check if the member is a manager.

        :param request: The HTTP request object.
        :param view: The API view being accessed.
        :return: True if the member is a manager, False otherwise.
        """
        return request.user.is_manager


class IsManagerOrReadOnlyOwnProfile(BasePermission):
    """
    Custom permission class for controlling access to member profiles.

    This permission class allows access to member profiles
    under the following conditions:
    — If the member is a manager (has 'is_manager' attribute set to True),
        they have full access.
    — If the view action is 'retrieve' (for viewing a specific profile),
        any authenticated member can access it.
    — Non-managers can only access their own profile.
    """

    def has_permission(self, request, view):
        """
        Check if the member has permission to access the view.

        :param request: The HTTP request object.
        :param view: The API view being accessed.
        :return: True if the member has permission, False otherwise.
        """
        return request.user.is_manager or view.action == 'retrieve'

    def has_object_permission(self, request, view, obj):
        """
        Check if the member has permission to access the member profile.
        Non-managers can only access their own profile.

        :param request: The HTTP request object.
        :param view: The API view being accessed.
        :param obj: Member profile being accessed.
        :return: True if the member has permission, False otherwise.
        """
        return request.user.is_manager or obj == request.user


class IsManagerOrReadOnlyOwnTeam(BasePermission):
    """
    Custom permission class for controlling access to team details.

    This permission class allows access to team details
    under the following conditions:
    — If the member is a manager (has 'is_manager' attribute set to True),
        they have full access.
    — If the view action is 'retrieve' (for viewing a specific team),
        any authenticated member can access it.
    — Non-managers can only access teams to which they are assigned as members.
    """

    def has_permission(self, request, view):
        """
        Check if the member has permission to access the view.

        :param request: The HTTP request object.
        :param view: The API view being accessed.
        :return: True if the member has permission, False otherwise.
        """
        return request.user.is_manager or view.action == 'retrieve'

    def has_object_permission(self, request, view, obj):
        """
        Check if the member has permission to access the specific team.
        Non-managers can only access teams to which they are assigned as members.

        :param request: The HTTP request object.
        :param view: The API view being accessed.
        :param obj: The specific team object being accessed.
        :return: True if the member has permission, False otherwise.
        """
        return request.user.is_manager or obj.members.filter(id=request.user.id).exists()
