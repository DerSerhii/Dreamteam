from rest_framework import serializers

from ..models import Member, Team, TeamMembership


class MemberSerializer(serializers.ModelSerializer):
    """
    Serializer for the Member model.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Member
        fields = ('id', 'username', 'first_name', 'last_name', 'position', 'email', 'password')


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
