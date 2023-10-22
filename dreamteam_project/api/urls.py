"""
API URL Configuration Module.
"""

from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .API.views import (
    MembersAllViewSet,
    MembersAvailableView,
    MemberPositionView,
    TeamViewSet,
    TeamMemberAddAPIView,
    TeamMemberDeleteView,
    LogoutView,
    LogoutAllView
)

router = routers.DefaultRouter()
router.register(r'all-members', MembersAllViewSet, basename='member')
router.register(r'teams', TeamViewSet)

urlpatterns = [
    # Resource URLs
    path('member-positions/', MemberPositionView.as_view(), name='member-positions'),
    path('available-members/', MembersAvailableView.as_view(), name='available-members'),
    path('team-add-member/', TeamMemberAddAPIView.as_view(), name='team-member-add'),
    path('team-delete-member/<int:pk>/', TeamMemberDeleteView.as_view(), name='team-member-delete'),
    path('', include(router.urls)),

    # Authentication URLs
    path('login/token/', TokenObtainPairView.as_view()),
    path('login/token/refresh/', TokenRefreshView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('logout-all/', LogoutAllView.as_view()),
]
