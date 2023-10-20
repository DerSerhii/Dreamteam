"""
API URL Configuration Module.
"""

from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .API.resources import (
    MemberViewSet,
    MemberPositionView,
    TeamViewSet,
    TeamMembershipViewSet
)

router = routers.DefaultRouter()
router.register(r'members', MemberViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'team_membership', TeamMembershipViewSet)

urlpatterns = [
    # Authentication URL
    path('login/token/', TokenObtainPairView.as_view()),
    path('login/token/refresh/', TokenRefreshView.as_view()),

    path('member-positions/', MemberPositionView.as_view()),

    # to router
    path('', include(router.urls))
]
