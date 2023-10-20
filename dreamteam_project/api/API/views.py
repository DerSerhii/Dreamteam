from django.db.models import Prefetch
from rest_framework import viewsets, views, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Member, Team, TeamMembership, MemberPosition
from .permissions import IsManager
from .serializers import (
    MemberSerializer,
    TeamSerializer,
    TeamMembershipSerializer,
)


class MemberViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsManager)
    queryset = Member.objects.only(
        'username',
        'first_name',
        'last_name',
        'position',
        'email',
    )
    serializer_class = MemberSerializer


class TeamViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsManager)
    queryset = Team.objects.prefetch_related(
        Prefetch('memberships',
                 queryset=TeamMembership.objects.select_related('member')
                 )
    )
    serializer_class = TeamSerializer


class TeamMemberAddAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsManager)
    serializer_class = TeamMembershipSerializer


class TeamMembershipDeleteView(generics.DestroyAPIView):
    queryset = TeamMembership.objects.only('id')
    serializer_class = TeamMembershipSerializer
    permission_classes = (IsAuthenticated, IsManager)


class MemberPositionView(views.APIView):
    def get(self, request):
        data = dict(MemberPosition.choices)
        return Response(data)
