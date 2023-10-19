from rest_framework import serializers

from ..models import Member


class MemberSerializer(serializers.ModelSerializer):
    """
    Serializer for the Member model.
    """

    class Meta:
        model = Member
        fields = ('username', 'first_name', 'last_name', 'position', 'email')
