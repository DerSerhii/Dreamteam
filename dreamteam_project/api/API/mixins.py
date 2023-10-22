"""
The module represents CUSTOM MIXIN class used in the project.
"""

from ..models import Member


class MemberMixin:
    """
    Mixin for different Member views that provides
    a pre-defined queryset for Member model.
    """

    def get_queryset(self):
        """
        Retrieves a queryset for Member model with selected fields
        and team memberships prefetched.

        :return: A queryset for Member model.
        """
        return Member.objects.only(
            'username',
            'first_name',
            'last_name',
            'position',
            'email'
        ).prefetch_related('team_memberships__team')
