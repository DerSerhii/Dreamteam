"""
API URL Configuration Module.
"""

from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views

from .API.resources import (
    MemberViewSet,
    TeamViewSet,
    TeamMembershipViewSet
)

router = routers.DefaultRouter()
router.register(r'members', MemberViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'team_membership', TeamMembershipViewSet)

urlpatterns = [
    # Authentication URL
    path('token-auth/', views.obtain_auth_token),

    # to router
    path('', include(router.urls))
]
