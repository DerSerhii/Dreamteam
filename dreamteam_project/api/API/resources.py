from rest_framework import viewsets, views
from rest_framework.response import Response

from ..models import Member, Team, TeamMembership, MemberPosition
from .serializers import (
    MemberSerializer,
    TeamSerializer,
    TeamMembershipSerializer
)


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.only(
        'username',
        'first_name',
        'last_name',
        'position',
        'email',
    )
    serializer_class = MemberSerializer


class MemberPositionView(views.APIView):
    def get(self, request):
        data = dict(MemberPosition.choices)
        return Response(data)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamMembershipViewSet(viewsets.ModelViewSet):
    queryset = TeamMembership.objects.all()
    serializer_class = TeamMembershipSerializer
