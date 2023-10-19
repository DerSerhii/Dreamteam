from rest_framework import viewsets

from ..models import Member
from .serializers import (
    MemberSerializer,
)


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.only(
        'username',
        'first_name',
        'last_name',
        'position',
        'email',
    )
    serializer_class = MemberSerializer
    # permission_classes = (IsAdminOrReadOnly,)
