from django.db.models import Q
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from api.API.serializers import TeamViewSerializer, MembersViewSerializer
from api.models import Member, Team, MemberPosition, TeamMembership


class TeamViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.member = Member.objects.create(username="testuser", position="PM", password="testpassword")
        self.team = Team.objects.create(name="Test Team")

    def test_get_teams(self):
        url = reverse("team-list")
        self.client.force_authenticate(self.member)
        response = self.client.get(url)
        teams = Team.objects.all()
        serializer = TeamViewSerializer(teams, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_team(self):
        url = reverse("team-list")
        data = {"name": "New Team"}
        self.client.force_authenticate(user=self.member)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_team(self):
        url = reverse("team-detail", args=[self.team.id])
        data = {"name": "Updated Team"}
        self.client.force_authenticate(user=self.member)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_team(self):
        url = reverse("team-detail", args=[self.team.id])
        self.client.force_authenticate(user=self.member)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class MembersAvailableViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.member = Member.objects.create(username="testuser", position="PM", password="testpassword")
        self.team = Team.objects.create(name="Test Team")
        self.url = reverse("member-list")

    def test_get_available_members(self):
        self.client.force_authenticate(user=self.member)
        response = self.client.get(self.url)
        members = Member.objects.exclude(
            Q(position__in=MemberPosition.only_one_team(), team_memberships__isnull=False)
            | ~Q(position__in=[choice[0] for choice in MemberPosition.choices])
        )
        serializer = MembersViewSerializer(members, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MembersAllViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.member = Member.objects.create(username="testuser", position="PM", password="testpassword")
        self.team = Team.objects.create(name="Test Team")
        self.url = reverse("member-list")

    def test_get_all_members(self):
        self.client.force_authenticate(user=self.member)
        response = self.client.get(self.url)
        members = Member.objects.all()
        serializer = MembersViewSerializer(members, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TeamMemberAddAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.member = Member.objects.create(username="testuser", position="PM", password="testpassword")
        self.team = Team.objects.create(name="Test Team")
        self.url = reverse("team-member-add")

    def test_add_member_to_team(self):
        self.client.force_authenticate(user=self.member)
        data = {"member": self.member.id, "team": self.team.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TeamMemberDeleteViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.member = Member.objects.create(username="testmember", position="PM", password="testpassword")
        self.team = Team.objects.create(name="Test Team")
        self.team_membership = TeamMembership.objects.create(member=self.member, team=self.team)
        self.url = reverse("team-member-delete", args=[self.team_membership.id])

    def test_delete_member_from_team(self):
        self.client.force_authenticate(user=self.member)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
