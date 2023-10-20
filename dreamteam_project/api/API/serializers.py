from rest_framework import serializers

from ..models import Member, MemberPosition, Team, TeamMembership


class MemberSerializer(serializers.ModelSerializer):
    """
    Serializer for the Member model.
    """

    class Meta:
        model = Member
        fields = ('id', 'username', 'first_name', 'last_name', 'position', 'email')


class TeamSerializer(serializers.ModelSerializer):
    """
    Serializer for the Team model.
    """
    members = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ('id', 'name', 'members')


class TeamMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMembership
        fields = '__all__'
