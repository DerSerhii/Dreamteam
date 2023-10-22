from django.utils.translation import gettext as _
from rest_framework import serializers

from ..models import Member, MemberPosition, Team, TeamMembership


class TeamMembershipEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMembership
        fields = '__all__'

    def validate(self, data):
        member = data.get('member')
        member_position = member.position

        if member_position in MemberPosition.only_one_team():
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

        if not member_position:
            error_message = _('Members without a position cannot be added to the team')
            raise serializers.ValidationError({'member': error_message})

        return data


class MemberInTeamSerializer(serializers.ModelSerializer):
    """
    # Serializer for the Member model.
    """

    class Meta:
        model = Member
        fields = ('username', 'first_name', 'last_name', 'position')


class TeamMembershipSerializer(serializers.ModelSerializer):
    member = MemberInTeamSerializer()

    class Meta:
        model = TeamMembership
        fields = ('id', 'date_joined', 'member')


class TeamSerializer(serializers.ModelSerializer):
    """
    Serializer for the Team model.
    """
    members = TeamMembershipSerializer(source='memberships', many=True, read_only=True)

    class Meta:
        model = Team
        fields = ('id', 'name', 'members')


class TeamForMembersSerializer(serializers.ModelSerializer):
    team = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TeamMembership
        fields = ('id', 'team')


class MembersViewSerializer(serializers.ModelSerializer):
    """
    # Serializer for the Member model.
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
