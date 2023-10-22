from django.test import TestCase
from rest_framework.exceptions import ValidationError

from api.models import Member, Team, TeamMembership
from api.API.serializers import (
    TeamMembershipEditSerializer,
    MemberInTeamSerializer,
    TeamMembershipSerializer,
    TeamViewSerializer,
    TeamForMembersSerializer,
    MembersViewSerializer
)


class TeamMembershipEditSerializerTest(TestCase):
    def test_team_membership_edit_serializer_valid_data(self):
        member = Member.objects.create(username="testmember", position="INT")
        team = Team.objects.create(name="Test Team")
        data = {"member": member.id, "team": team.id}
        serializer = TeamMembershipEditSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_team_membership_edit_serializer_invalid_data(self):
        member = Member.objects.create(username="testmember", position="INT")
        team = Team.objects.create(name="Test Team")
        # Attempt to create a duplicate team membership
        TeamMembership.objects.create(member=member, team=team)
        data = {"member": member.id, "team": team.id}
        serializer = TeamMembershipEditSerializer(data=data)
        self.assertRaises(ValidationError)


class MemberInTeamSerializerTest(TestCase):
    def test_member_in_team_serializer(self):
        member = Member.objects.create(username="testmember", position="INT")
        serializer = MemberInTeamSerializer(member)
        expected_fields = ["username", "first_name", "last_name", "position"]
        self.assertEqual(list(serializer.data.keys()), expected_fields)


class TeamMembershipSerializerTest(TestCase):
    def test_team_membership_serializer(self):
        member = Member.objects.create(username="testmember", position="INT")
        team = Team.objects.create(name="Test Team")
        membership = TeamMembership.objects.create(member=member, team=team)
        serializer = TeamMembershipSerializer(membership)
        expected_fields = ["id", "date_joined", "member"]
        self.assertEqual(list(serializer.data.keys()), expected_fields)


class TeamViewSerializerTest(TestCase):
    def test_team_view_serializer(self):
        team = Team.objects.create(name="Test Team")
        serializer = TeamViewSerializer(team)
        expected_fields = ["id", "name", "members"]
        self.assertEqual(list(serializer.data.keys()), expected_fields)


class TeamForMembersSerializerTest(TestCase):
    def test_team_for_members_serializer(self):
        member = Member.objects.create(username="testmember", position="INT")
        team = Team.objects.create(name="Test Team")
        TeamMembership.objects.create(member=member, team=team)
        serializer = TeamForMembersSerializer(team.memberships.all(), many=True)
        expected_fields = ["id", "team"]
        self.assertEqual(list(serializer.data[0].keys()), expected_fields)


class MembersViewSerializerTest(TestCase):
    def test_members_view_serializer(self):
        member = Member.objects.create(username="testmember", position="INT")
        serializer = MembersViewSerializer(member)
        expected_fields = ["id", "username", "first_name", "last_name", "position", "email", "teams"]
        self.assertEqual(list(serializer.data.keys()), expected_fields)
