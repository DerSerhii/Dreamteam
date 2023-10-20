"""
API URL Configuration Module.
"""

from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .API.views import (
    MemberViewSet,
    MemberPositionView,
    TeamViewSet,
    TeamMemberAddAPIView,
    TeamMembershipDeleteView
)

router = routers.DefaultRouter()
router.register(r'members', MemberViewSet)
router.register(r'teams', TeamViewSet)

urlpatterns = [
    # Authentication URL
    path('login/token/', TokenObtainPairView.as_view()),
    path('login/token/refresh/', TokenRefreshView.as_view()),

    path('member-positions/', MemberPositionView.as_view()),
    path('team-add-member/', TeamMemberAddAPIView.as_view()),
    path('team-delete-member/<int:pk>/', TeamMembershipDeleteView.as_view()),

    # to router
    path('', include(router.urls))
]
