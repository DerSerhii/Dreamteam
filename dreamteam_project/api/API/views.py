from django.db import transaction
from django.db.models import Prefetch, Q
from rest_framework import viewsets, views, generics, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken
)

from ..models import Team, TeamMembership, MemberPosition
from .mixins import MemberMixin
from .permissions import (
    IsManager,
    IsManagerOrReadOnlyOwnProfile,
    IsManagerOrReadOnlyOwnTeam
)
from .serializers import (
    MembersViewSerializer,
    TeamSerializer,
    TeamMembershipEditSerializer,
)


class TeamViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsManagerOrReadOnlyOwnTeam)
    serializer_class = TeamSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    queryset = Team.objects.prefetch_related(
        Prefetch(
            'memberships',
            queryset=TeamMembership.objects.select_related('member')
        )
    )


class MembersAvailableView(MemberMixin, generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsManager)
    serializer_class = MembersViewSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.exclude(
            Q(position__in=MemberPosition.only_one_team(), team_memberships__isnull=False)
            | ~Q(position__in=list(map(lambda choice: choice[0], MemberPosition.choices)))
        )


class MembersAllViewSet(MemberMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsManagerOrReadOnlyOwnProfile)
    serializer_class = MembersViewSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('username', 'first_name', 'last_name', 'position')


class TeamMemberAddAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsManager)
    serializer_class = TeamMembershipEditSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class TeamMembershipDeleteView(generics.DestroyAPIView):
    queryset = TeamMembership.objects.only('id')
    serializer_class = TeamMembershipEditSerializer
    permission_classes = (IsAuthenticated, IsManager)


class MemberPositionView(views.APIView):
    def get(self, request):
        data = dict(MemberPosition.choices)
        return Response(data)


class LogoutView(views.APIView):

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)

        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(views.APIView):

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)
