"""
The module represents VIEWS (API resources) used in the project.
"""

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
    TeamViewSerializer,
    TeamMembershipEditSerializer,
)


class TeamViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing teams, including creation, retrieval,
    updating, and deletion of teams.

    Provides endpoints to perform CRUD operations on teams
    and includes filtering.
    """
    permission_classes = (IsAuthenticated, IsManagerOrReadOnlyOwnTeam)
    serializer_class = TeamViewSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    queryset = Team.objects.prefetch_related(
        Prefetch(
            'memberships',
            queryset=TeamMembership.objects.select_related('member')
        )
    )


class MembersAvailableView(MemberMixin, generics.ListAPIView):
    """
    A view that provides a list of available members to add to teams.

    Allows find members who meet certain positions and are not part of any team,
    if they have positions that prohibit being on multiple teams.
    """
    permission_classes = (IsAuthenticated, IsManager)
    serializer_class = MembersViewSerializer

    def get_queryset(self):
        """
        Retrieves the queryset for Member model with available members,
        excluding:
        — members who already have a team and are not allowed to be in several;
        — members whose position does not correspond to what is permitted
            (for example, the superuser is initialized with an empty position,
            it can be used for a situation where there are no managers,
            but as such it is not a member).

        """
        queryset = super().get_queryset()

        return queryset.exclude(
            Q(position__in=MemberPosition.only_one_team(), team_memberships__isnull=False)
            | ~Q(position__in=list(map(lambda choice: choice[0], MemberPosition.choices)))
        )


class MembersAllViewSet(MemberMixin, viewsets.ModelViewSet):
    """
    Viewset for managing members, including creation, retrieval,
    updating, and deletion of members.

    Provides endpoints to perform CRUD operations on teams
    and includes filtering.
    """
    permission_classes = (IsAuthenticated, IsManagerOrReadOnlyOwnProfile)
    serializer_class = MembersViewSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('username', 'first_name', 'last_name', 'position')


class TeamMemberAddAPIView(generics.CreateAPIView):
    """
    A view for adding members to teams.

    Allows adding members to teams by creating `TeamMembership` records.
    It enforces permission checks to ensure only authenticated member
    with 'is_manager' access can add members to teams.
    """
    permission_classes = (IsAuthenticated, IsManager)
    serializer_class = TeamMembershipEditSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # In validation serializers is select_for_update()
        # see validate() TeamMembershipEditSerializer
        return super().create(request, *args, **kwargs)


class TeamMemberDeleteView(generics.DestroyAPIView):
    """
    A view for deleting members to teams.

    Allows deleting members to teams by creating `TeamMembership` records.
    It enforces permission checks to ensure only authenticated member
    with 'is_manager' access can add members to teams.
    """
    queryset = TeamMembership.objects.only('id')
    serializer_class = TeamMembershipEditSerializer
    permission_classes = (IsAuthenticated, IsManager)


class MemberPositionView(views.APIView):
    """
    A view for retrieving the available member positions.
    """

    def get(self, request):
        """
        Handled GET requests to retrieve member positions.
        """
        data = dict(MemberPosition.choices)
        return Response(data)


class LogoutView(views.APIView):
    """
     A view for user logout and token blacklisting.
    """

    def post(self, request):
        """
        Handles POST requests for user logout and token blacklisting.
        """
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(views.APIView):
    """
    A view for user logout from all active sessions and token blacklisting.
    """

    def post(self, request):
        """
        Handles POST requests for user logout from all sessions and token blacklisting.
        """
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)
        return Response(status=status.HTTP_205_RESET_CONTENT)
