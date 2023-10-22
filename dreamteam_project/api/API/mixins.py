from ..models import Member


class MemberMixin:
    def get_queryset(self):
        return Member.objects.only(
            'username',
            'first_name',
            'last_name',
            'position',
            'email'
        ).prefetch_related('team_memberships__team')
