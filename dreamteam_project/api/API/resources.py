from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Member, Team, TeamMembership
from .serializers import (
    MemberSerializer,
    TeamSerializer,
    TeamMembershipSerializer
)


class MemberViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Member.objects.only(
        'username',
        'first_name',
        'last_name',
        'position',
        'email',
    )
    serializer_class = MemberSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamMembershipViewSet(viewsets.ModelViewSet):
    queryset = TeamMembership.objects.all()
    serializer_class = TeamMembershipSerializer
