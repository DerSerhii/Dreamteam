"""
The module represents SERIALIZERS used in the project.
"""

from django.utils.translation import gettext as _
from rest_framework import serializers

from ..models import Member, MemberPosition, Team, TeamMembership


class TeamMembershipEditSerializer(serializers.ModelSerializer):
    """
    Serializer for TeamMembership model for editing team composition,
    used in view to add or remove members to teams
    (create or delete TeamMembership instances).

    Additional validation:
    — Members with positions requiring a single team
        cannot be added to multiple teams.
    — Members without a specified position can't be added to a team.
    """

    class Meta:
        model = TeamMembership
        fields = '__all__'

    def validate(self, data):
        member = data.get('member')
        member_position = member.position

        # Check if the member is already in another team (only one-team members).
        if member_position in MemberPosition.only_one_team():
            # This query inside transaction
            # see create() TeamMemberAddAPIView
            team_member = (
                TeamMembership.objects.select_for_update().
                select_related('team').filter(member=member).first()
            )
            if team_member:
                first_name = member.first_name
                last_name = member.last_name
                full_name = f"{first_name} {last_name} ({member_position})"
                team = team_member.team.name
                error_message = _(f"{full_name} already exists in the {team} team")
                raise serializers.ValidationError({'member': error_message})

        # Check if the member without a specified position.
        if not member_position:
            error_message = _('Members without a position cannot be added to the team')
            raise serializers.ValidationError({'member': error_message})

        return data


class MemberInTeamSerializer(serializers.ModelSerializer):
    """
    Serializer for Member model,
    customized for use in TeamMembershipSerializer.
    """

    class Meta:
        model = Member
        fields = ('username', 'first_name', 'last_name', 'position')


class TeamMembershipSerializer(serializers.ModelSerializer):
    """
    Serializer for TeamMembership model,
    customized for use in TeamMembershipSerializer.
    """
    member = MemberInTeamSerializer()

    class Meta:
        model = TeamMembership
        fields = ('id', 'date_joined', 'member')


class TeamViewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Team model, designed for the Team view set.

    Note:
    — `members` is represented as a list of team memberships,
        which includes details about the team members.
    """
    members = TeamMembershipSerializer(source='memberships', many=True, read_only=True)

    class Meta:
        model = Team
        fields = ('id', 'name', 'members')


class TeamForMembersSerializer(serializers.ModelSerializer):
    """
    Serializer for TeamMembership model,
    customized for use in MembersViewSerializer.
    """
    team = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TeamMembership
        fields = ('id', 'team')


class MembersViewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Member model, designed for the Member view sets.

    Note:
     — `teams` is represented as a list of teams to which the member belongs.
     — `password` is a write-only field for setting or updating the member's password.
    """
    teams = TeamForMembersSerializer(source='team_memberships', many=True, read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Member
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'position',
            'email',
            'teams',
            'password'
        )
